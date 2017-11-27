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
   GROUP BY articles.slug) subqr ON a.slug = subqr.slug
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
   GROUP BY author) p ON a.id = p.author
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
