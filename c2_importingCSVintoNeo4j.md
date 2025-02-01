# Importing CSV data into Neo4j

## Loading CSV file
```ruby
LOAD CSV WITH HEADERS 
FROM 'https://data.neo4j.com/importing-cypher/people.csv' AS row
RETURN row
```
```ruby
LOAD CSV 
FROM 'file:///data.csv' AS line FIELDTERMINATOR '$'
```

## counting rows
```ruby
LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/people.csv'
as row
RETURN count(row)
```

## Nodes

```ruby
LOAD CSV WITH HEADERS 
FROM 'https://data.neo4j.com/importing-cypher/persons.csv' AS row
MERGE (p:Person {tmdbId: toInteger(row.person_tmdbId)})
SET
p.imdbId = toInteger(row.person_imdbId),
p.bornIn = row.bornIn,
p.name = row.name,
p.bio = row.bio,
p.poster = row.poster,
p.url = row.url,
p.born = row.born,
p.died = row.died
```

Merge >> create a node
SET >> declare properties in the node

## Unique IDs and constraints

### Create a constraints
```ruby
CREATE CONSTRAINT [constraint_name] [IF NOT EXISTS]
FOR (n:LabelName)
REQUIRE n.propertyName IS UNIQUE
```

```ruby
CREATE CONSTRAINT Person_tmdbId
FOR (x:Person) 
REQUIRE x.tmdbId IS UNIQUE
```

### Drop a constraints
DROP CONSTRAINT [constraint_name]

### show a constraints
SHOW CONSTRAINTS


### Exercise - creating movie nodes
```ruby
LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/movies.csv' AS row
MERGE (m:Movie{movieId:toInteger(row.movieId)})
SET
m.tmdbId = toInteger(row.movie_tmdbId),
m.imdbId = toInteger(row.movie_imdbId),
m.released = row.released,
m.title = row.title,
m.year = row.year,
m.plot = row.plot,
m.budget = row.budget
```
```ruby
CREATE CONSTRAINT Movie_movieId
FOR (m:Movie)
REQUIRE m.movieId IS UNIQUE
```

## Relationships
Review the Cypher statement below, which creates the ACTED_IN relationships between the Person and Movie nodes.
```ruby
LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/acted_in.csv' AS row
MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
MATCH (m:Movie {movieId: toInteger(row.movieId)})
MERGE (p)-[r:ACTED_IN]->(m)
SET r.role = row.role
```

## Data Types

### Casting
The types of data that you can store as properties in Neo4j include:

- String
- Integer
- Float (decimal values)
- Boolean
- Date/Datetime
- Point (spatial)
- Lists of values 

```ruby
MERGE (p:Person {tmdbId: toInteger(row.person_tmdbId)})
SET
p.imdbId = toInteger(row.person_imdbId)
```

| Function    | Description                         |
|------------|-------------------------------------|
| toBoolean() | Converts a string to a boolean value |
| toFloat()   | Converts a string to a float value   |
| toInteger() | Converts a string to an integer value |
| toString()  | Converts a value to a string        |
| date()      | Converts a string to a date value   |
| datetime()  | Converts a string to a date and time value |

function to show the data types used in the graph:
```ruby
CALL apoc.meta.nodeTypeProperties()
YIELD nodeType, propertyName, propertyTypes
```

## Lists

### The split function
The split function will transform a string value into a list. The split function takes two arguments:
- The string to split
- The character to split on  
```ruby
LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/movies.csv'
AS row
MERGE (m:Movie {movieId: toInteger(row.movieId)})
SET
m.tmdbId = toInteger(row.movie_tmdbId),
m.imdbId = toInteger(row.movie_imdbId),
m.released = date(row.released),
m.title = row.title,
m.year = toInteger(row.year),
m.plot = row.plot,
m.budget = toInteger(row.budget),
m.imdbRating = toFloat(row.imdbRating),
m.poster = row.poster,
m.runtime = toInteger(row.runtime),
m.imdbVotes = toInteger(row.imdbVotes),
m.revenue = toInteger(row.revenue),
m.url = row.url,
m.countries = split(row.countries, '|')
```

```ruby
MATCH (m:Movie)
WHERE "France" IN m.countries
RETURN m
```

## Labels
can add labels to a node using SET, the syntax is:
```ruby
MATCH(n)
SET n:Label 
```
add actor label
```ruby
MATCH (p:Person)-[:ACTED_IN]->()
WITH DISTINCT p 
SET p:Actor
```

## Importing data considerations
In this lesson, you will build a single import process to rebuild the graph by:  
- Deleting any existing data
- Dropping any existing constraints
- Run the queries to create the constraints, nodes, and relationships

### Multiple Queries
To run multiple queries together, you must put a semi-colon (;) at the end of each query.
For example, this Cypher code contains two separate queries which will run one after the other:
```ruby
MATCH (p:Person) RETURN p;
MATCH (m:Movie) RETURN m;
```

### resetting the data
1. delete relationships
```ruby
MATCH (Person)-[r:ACTED_IN]->(Movie) DELETE r;
MATCH (Person)-[r:DIRECTED]->(Movie) DELETE r;
```

2. delete the nodes
```ruby
MATCH (p:Person) DELETE p;
MATCH (m:Movie) DELETE m;
```

```ruby
MATCH (p:Person) DETACH DELETE p;
MATCH (m:Movie) DETACH DELETE m;
```

3. drop the constraints
```ruby
DROP CONSTRAINT Person_tmdbId IF EXISTS;
DROP CONSTRAINT Movie_movieId IF EXISTS;
```

4. Importing te data
```ruby
MATCH (p:Person) DETACH DELETE p;
MATCH (m:Movie) DETACH DELETE m;

DROP CONSTRAINT Person_tmdbId IF EXISTS;
DROP CONSTRAINT Movie_movieId IF EXISTS;

CREATE CONSTRAINT Person_tmdbId IF NOT EXISTS
FOR (x:Person)
REQUIRE x.tmdbId IS UNIQUE;

CREATE CONSTRAINT Movie_movieId IF NOT EXISTS
FOR (x:Movie)
REQUIRE x.movieId IS UNIQUE;

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/persons.csv' AS row
MERGE (p:Person {tmdbId: toInteger(row.person_tmdbId)})
SET
p.imdbId = toInteger(row.person_imdbId),
p.bornIn = row.bornIn,
p.name = row.name,
p.bio = row.bio,
p.poster = row.poster,
p.url = row.url,
p.born = date(row.born),
p.died = date(row.died);

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/movies.csv' AS row
MERGE (m:Movie {movieId: toInteger(row.movieId)})
SET
m.tmdbId = toInteger(row.movie_tmdbId),
m.imdbId = toInteger(row.movie_imdbId),
m.released = date(row.released),
m.title = row.title,
m.year = toInteger(row.year),
m.plot = row.plot,
m.budget = toInteger(row.budget),
m.imdbRating = toFloat(row.imdbRating),
m.poster = row.poster,
m.runtime = toInteger(row.runtime),
m.imdbVotes = toInteger(row.imdbVotes),
m.revenue = toInteger(row.revenue),
m.url = row.url,
m.countries = split(row.countries, '|'),
m.languages = split(row.languages, '|');

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/acted_in.csv' AS row
MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
MATCH (m:Movie {movieId: toInteger(row.movieId)})
MERGE (p)-[r:ACTED_IN]->(m)
SET r.role = row.role;

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/directed.csv' AS row
MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
MATCH (m:Movie {movieId: toInteger(row.movieId)})
MERGE (p)-[r:DIRECTED]->(m);

MATCH (p:Person)-[:ACTED_IN]->()
WITH DISTINCT p SET p:Actor;

MATCH (p:Person)-[:DIRECTED]->()
WITH DISTINCT p SET p:Director;
```

# cypher query
```ruby
CREATE CONSTRAINT Person_tmdbId IF NOT EXISTS
FOR (x:Person)
REQUIRE x.tmdbId IS UNIQUE;

CREATE CONSTRAINT Movie_movieId IF NOT EXISTS
FOR (x:Movie)
REQUIRE x.movieId IS UNIQUE;

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/persons.csv' AS row
MERGE (p:Person {tmdbId: toInteger(row.person_tmdbId)})
SET
p.imdbId = toInteger(row.person_imdbId),
p.bornIn = row.bornIn,
p.name = row.name,
p.bio = row.bio,
p.poster = row.poster,
p.url = row.url,
p.born = date(row.born),
p.died = date(row.died);

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/movies.csv' AS row
MERGE (m:Movie {movieId: toInteger(row.movieId)})
SET
m.tmdbId = toInteger(row.movie_tmdbId),
m.imdbId = toInteger(row.movie_imdbId),
m.released = date(row.released),
m.title = row.title,
m.year = toInteger(row.year),
m.plot = row.plot,
m.budget = toInteger(row.budget),
m.imdbRating = toFloat(row.imdbRating),
m.poster = row.poster,
m.runtime = toInteger(row.runtime),
m.imdbVotes = toInteger(row.imdbVotes),
m.revenue = toInteger(row.revenue),
m.url = row.url,
m.countries = split(row.countries, '|'),
m.languages = split(row.languages, '|');

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/acted_in.csv' AS row
MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
MATCH (m:Movie {movieId: toInteger(row.movieId)})
MERGE (p)-[r:ACTED_IN]->(m)
SET r.role = row.role;

LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/importing-cypher/directed.csv' AS row
MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
MATCH (m:Movie {movieId: toInteger(row.movieId)})
MERGE (p)-[r:DIRECTED]->(m);

MATCH (p:Person)-[:ACTED_IN]->()
WITH DISTINCT p SET p:Actor;

MATCH (p:Person)-[:DIRECTED]->()
WITH DISTINCT p SET p:Director;
```

