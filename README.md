## Fragile Families Metadata

[![Build Status](https://travis-ci.org/fragilefamilieschallenge/metadata_app.svg?branch=master)](https://travis-ci.org/fragilefamilieschallenge/metadata_app)

This is a Python Flask app that provides a GUI for searching and browsing metadata on FFCWS variables.

This app also provides access to the Fragile Families Metadata through HTTP endpoints that return JSON results. The web endpoints allow web users to query, select and filter the metadata variables in several ways.

Access to the 'raw' metadata CSV file is also provided. The latest CSV files are available in the 'data' folder of the ffmeta package.

The web interface is available at:
[http://metadata.fragilefamilies.princeton.edu](http://metadata.fragilefamilies.princeton.edu)

The API interface is made available at:
[http://api.metadata.fragilefamilies.princeton.edu](http://api.metadata.fragilefamilies.princeton.edu)

### Installation

The web interface and api can be used directly using the links above. However, if you wish to replicate the setup on your own servers:

1. Ensure Docker is installed and running.
2. `git clone https://github.com/fragilefamilieschallenge/metadata_app.git`
3. `cd metadata_app/`
4. Ensure gui.config.cfg (private keys file) exists in current directory.
5. `docker build -t metadata_app .`
6. `docker run -p 5000:5000 metadata_app` You may need to change the second port number if you're running multiple Flask apps in Docker containers

## API

The Base URI for the API interface is:
[http://api.metadata.fragilefamilies.princeton.edu](http://api.metadata.fragilefamilies.princeton.edu)

At this URI, we provide 2 API endpoints:

### Select
If you know the name of the variable you're interested in, this endpoint is to be used to retrieve metadata for a variable, given its name.

#### Returns metadata for variable with name \<varName\>.
General Format: `/variable/<varName>`

`/variable/m1a3`
```
{
    "data_source": "questionnaire",
    "data_type": "bin",
    "fp_PCG": 0,
    "fp_father": 0,
    "fp_fchild": 1,
    "fp_mother": 1,
    "fp_other": 0,
    "fp_partner": 0,
    "group_id": "221",
    "group_subid": null,
    "id": 85890,
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?",
    "leaf": "3",
    "measures": null,
    "name": "m1a3",
    "old_name": "m1a3",
    "probe": null,
    "qText": null,
    "respondent": "Mother",
    "responses": {
        "1": "Yes",
        "2": "No",
        "-9": "Not in wave",
        "-8": "Out of range",
        "-7": "N/A",
        "-6": "Skip",
        "-5": "Not asked",
        "-4": "Multiple ans",
        "-3": "Missing",
        "-2": "Don't know",
        "-1": "Refuse"
    },
    "scope": "20",
    "section": "a",
    "survey": "m",
    "topics": [
        {
            "topic": "parenting abilities",
            "umbrella": "Parenting"
        }
    ],
    "warning": 0,
    "wave": "1"
}
```

#### Optionally, if you also know the name of the field(s) you're interested in, it can return data corresponding to these field(s).

General Format: `/variable/<varName>?<fieldName>` or `/variable/<varName>?<fieldName1>&<fieldName2>&<fieldName3>..`

`/variable/m1a3?label`
```
{
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?"
}
```

`/variable/m1a3?label&data_source`
```
{
    "data_source": "questionnaire",
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?"
}
```

### Search
You can search for variables given one or more search criteria.

#### General Format
`/variable?q={"filters":[<filter>, <filter>, ..]}`

where `<filter>` is an individual filter, described below.

#### `filter` Specification

A `filter` is a dictionary of the form `{"name":<attributeName>,"op":<operator>,"val":<value>}`
 
`<attributeName>` is the name of the attribute that forms the basis for the search.

`<operator>` is the comparison *operator* for the search. The most commonly used operators are `eq` (for exact comparison) and `like` (for fuzzy comparison).

`<value>` is the value against which you want the comparison to work.

##### Supported Operators

**eq**: equals
    
    Search for variables where "name" is exactly "m1a3"
    {"name":"name","op":"eq","val":"m1a3"}

**like**: search for a pattern

With the `like` operator, you can use the `%` character to match any character.

    Search for variables where "name" starts with "f1"
    {"name":"name","op":"like","val":"f1%"}

    Search for variables where "qText" has the word "financial" somewhere in it
    {"name":"qText","op":"like","val":"%financial%"}

**lt**: less-than, **le**: less-than-or-equal-to, **gt**: greater-than, **gte**: greater-than-or-equal-to
    
    Search for variables where "warning" <= 1
    {"name":"warning","op":"leq","val":"m1a3"}

**neq**: not equals
    
    Search for variables where "data_source" is not "questionnaire"
    {"name":"data_source","op":"neq","val":"questionnaire"}

**in**: is in (is one of ..)
    
    Search for variables where "respondent" is in ["Father", "Mother"] (i.e. it is either "Father" or "Mother")
    {"name":"respondent","op":"in","val":["Father","Mother"]}

**not_in**: is not in (is not any of ..)
    
    Search for variables where "wave" is neither "Year 1" nor "Year 3"
    {"name":"wave","op":"no_in","val":["Year 1","Year 3"]}

**is_null**: is null (is missing)

**is_not_null**: is not null (is not missing)

For most fields, a special "null" value denotes a missing value.

    Search for variables where "wave" is missing
    {"name":"wave","op":"is_null"}

For certain fields (e.g. "focal_person"), the "null" value denotes **no** focal person.

    Search for variables where there is a "focal_person"
    {"name":"focal_person","op":"is_not_null"}

For `is_null` and `is_not_null` operators, you need not supply a `val`, since it has no meaning. (A `val` is ignored if found).

#### Multiple Filters

It is possible to search on multiple criteria, simply by providing more than one `filter`.

    Search for variables where "wave" is "Year 1" and "name" starts with "f"
    /variable?q={"filters":[{"name":"wave,"op":"eq","val":"Year 1"}, {"name":"name,"op":"like","val":"f%"}]}

##### OR Filters

By default, `filters` is a list of individual filters, combined using the **AND** operation (i.e. all filter conditions must be met), as in the example above.

To specify an **OR** operation on multiple filters, `filters` can be specified as a dictionary instead, with the key "or", and the values as a list of individual `filter` objects. For example:

    Search for variables where "wave" is "Year 5" or "respondent" is "Father"
    /variable?q={"filters":{"or": [{"name":"wave,"op":"eq","val":"Year 5"}, {"name":"respondent,"op":"eq","val":"Father"}] }}

More complicated search criteria involving multiple and nested AND/OR filters can be constructed in the same way. In these cases, you may find that using the interactive <a href="http://metadata.fragilefamilies.princeton.edu/search">Advanced Search Tool</a> helpful, which generates and displays the API call corresponding to the search.

##### Notes

  - Note that `val` field in a `filter` needs to be the literal value that you're searching for. It cannot be the name of another attribute (i.e. you cannot search for variables where `name` is equal to `old_name`, for example.)
  - With most modern browsers, you can simply type or copy-paste URLs with characters like `%`, `[`, `]`, `{` in them. However, note that when using the API programmatically, you would need to properly <a href="https://en.wikipedia.org/wiki/Percent-encoding">URL Encode</a> your query string to the API endpoint. Most HTTP libraries will do this automatically for you, but this is something to be aware of.
  
## Errors

API calls can generate errors if not used correctly. In all such cases, the returned HTTP Response code is 400, indicating a Bad Request.

#### Getting the metadata for a variable that doesn't exist:

`/variable/m1a2` (no variable by name `m1a2` exists)

returns an HTTP 400 (Bad Request) Response with the message body:
```
{
    "message": "Invalid variable name."
}
```
