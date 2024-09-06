# RSS Parser for Scientific Articles

This project is a Python-based RSS parser that fetches and stores scientific articles from Nature and bioRxiv RSS feeds.

## What is RSS?

RSS (Really Simple Syndication) is a web feed that allows users and applications to access updates to websites in a standardized, computer-readable format. These feeds can, for example, allow a user to keep track of many different websites in a single news aggregator.

In the context of this project, we use RSS feeds from Nature and bioRxiv to automatically fetch the latest scientific articles and store them in a database.

## Features

- Parses RSS feeds from Nature and bioRxiv
- Stores article data in a DuckDB database
- [ ] Updates the database daily
- Handles errors and provides logging

## Installation
1. Clone this repository
2. Create a conda environment using the provided `environment.yml` file:

```
conda env create -f environment.yml
```

3. Activate the environment:

```
conda activate rss_parser
```

## Usage

Run the script with:

```
python rss_parser.py
```

The script will run continuously, updating the database daily at midnight.

## Database Schema

The script creates two tables in the DuckDB database:

1. `nature_articles`
2. `biorxiv_articles`

Both tables have the following schema:

- `title`: VARCHAR
- `publish_date`: TIMESTAMP
- `link`: VARCHAR
- `identifier`: VARCHAR
- `content`: VARCHAR
- `update_date`: DATE

## Error Handling

The script includes basic error handling and logging. Check the console output or log files for any issues.

## Contributing

Feel free to fork this repository and submit pull requests with any improvements.

## License

This project is licensed under the MIT License.