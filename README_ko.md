# 프로젝트: 사이트 로그 분석(Logs Analysis)

`logs_analysis.py` 스크립트는 _PostgreSQL_ 데이터베이스를 활용하여, 특정한 사이트의 접속로그 기록을 분석하고 SQL 질의문을 활용해 보고서를 작성하여 텍스트 형식으로 저장하는 분석 툴입니다.

## 스크립트 실행
[_PostgreSQL_](https://www.postgresql.org) 데이터베이스와 커멘드라인 소프트웨어가 설치되어 있어야 정상적으로 작동합니다.

1. 깃허브 저장소를 복제합니다: `git clone https://github.com/YoungsAppWorkshop/logsanalysis`
2. [사이트 로그 데이터를 다운로드](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) 후, 압축을 풀고 `newsdata.sql` 파일을 로그분석 스크립트가 있는 디렉토리에 저장합니다.
3. 로컬 데이터베이스에 사이트 로그 데이터를 로드합니다: `psql -d YOUR_DATABASE_NAME -f newsdata.sql`
4. 뷰(View)를 생성합니다: `psql -d YOUR_DATABASE_NAME -f views.sql`
5. 로그 분석 스크립트를 실행합니다.: `python3 logs_analysis.py`

## 파일 리스트
```bash
└── logsanalysis
    ├── logs_analysis.py    # 로그분석 보고서를 작성하는 파이썬 스크립트입니다.
    ├── README_ko.md        # 한글 README 파일
    ├── README.md           # 영문 README 파일
    ├── report.txt          # 보고서 생성 예시
    └── views.sql           # View 정의
```

## 뷰(View) 정의
사이트 로그 분석을 위해 아래의 뷰(View)들이 사용되었습니다. 뷰 정의는 `views.sql` 파일에도 포함되어 있습니다.
```
-- 1. 가장 인기있는 글 세 가지는 무엇인가?

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

-- 2. 가장 인기있는 작가는 누구인가?

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

-- 3. 클라이언트로부터의 요청 중 1% 이상 에러가 발생한 날은 언제인가?

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

## 라이센스
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
