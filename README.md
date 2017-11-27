# Project: Logs Analysis

`logs_analysis.py` is a reporting tool that connect to a _PostgreSQL_ database, execute SQL queries, and produce a plain text report file.

- 한글 리드미(README Korean) 파일: [README_ko.md](https://github.com/YoungsAppWorkshop/logsanalysis/blob/master/README_ko.md)

## How to Start

The [_PostgreSQL_](https://www.postgresql.org) database and support software needed for this project to work properly.

1. Clone the github repository: `git clone https://github.com/YoungsAppWorkshop/logsanalysis`
2. [Download logs data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) file, unzip it and store the `newsdata.sql` file in the directory.
3. Load the data into your local database: `psql -d YOUR_DATABASE_NAME -f newsdata.sql`
4. Create views: `psql -d YOUR_DATABASE_NAME -f views.sql`
5. Run the logs analysis script: `python3 logs_analysis.py`

## Structure
```bash
└── logsanalysis
    ├── logs_analysis.py    # A python script for generating logs analysis reports
    ├── README_ko.md        # Korean README file
    ├── README.md           # English README file
    ├── report.txt          # Sample report file
    └── views.sql           # View Definitions
```

## View Definitions
Following views are defined to answer the questions of the project. The view definitions are also included in `views.sql` file.
```
-- 1. What are the most popular three articles of all time?

CREATE VIEW article_popularity AS
SELECT a.id,
       a.title,
       a.slug,
       a.author,
       subqr.num_of_requests
FROM articles a
JOIN
  (SELECT articles.slug,
          count(log.path) AS num_of_requests
   FROM articles
   LEFT JOIN log ON log.path LIKE '%' || articles.slug
   GROUP BY articles.slug) subqr
ON a.slug = subqr.slug
ORDER BY subqr.num_of_requests DESC;

-- 2. Who are the most popular article authors of all time?

CREATE VIEW author_popularity AS
SELECT a.name AS author_name,
       coalesce(p.views, 0) AS total_views
FROM authors a
LEFT JOIN
  (SELECT sum(num_of_requests) AS views,
          author
   FROM article_popularity
   GROUP BY author) p
ON a.id = p.author
ORDER BY total_views DESC;

-- 3. On which days did more than 1% of requests lead to errors?

CREATE VIEW error_report AS
SELECT log_date,
       total_request,
       (total_request - error) AS non_error_cnt,
       error AS error_cnt,
       (error/total_request::float) AS error_rate
FROM
  (SELECT date(TIME) AS log_date,
          count(status) AS total_request,
          sum(CASE
                  WHEN status SIMILAR TO '(4|5)%' THEN 1
                  ELSE 0
              END ) AS error
   FROM log
   GROUP BY log_date ) subqr;
```

## License
This is a public domain work, dedicated using
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
