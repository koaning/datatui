# CLI

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

* `annotate`: Annotate and put some examples into the...
* `count`: Count and pretty print the number of...
* `export`: Export annotations from the cache.

## `annotate`

Annotate and put some examples into the cache.

**Usage**:

```console
$ annotate [OPTIONS] EXAMPLES_PATH
```

**Arguments**:

* `EXAMPLES_PATH`: [required]

**Options**:

* `--cache TEXT`: Cache path  [default: annotations]
* `--collection TEXT`: Attach a collection name to each annotation  [default: default]
* `--descr TEXT`: Add a description
* `--help`: Show this message and exit.

## `count`

Count and pretty print the number of annotations per collection.

**Usage**:

```console
$ count [OPTIONS]
```

**Options**:

* `--cache TEXT`: Cache path  [default: annotations]
* `--help`: Show this message and exit.

## `export`

Export annotations from the cache.

**Usage**:

```console
$ export [OPTIONS]
```

**Options**:

* `--cache TEXT`: Cache path  [default: annotations]
* `--collection TEXT`: Subset a collection
* `--file-out TEXT`: Output file path
* `--help`: Show this message and exit.

