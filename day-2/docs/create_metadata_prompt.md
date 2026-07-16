# MDSP Step 1: Load and Inspect a Dataset Locally

<!--
Purpose:
Use this prompt with a GenAI tool to generate a simple Python script for the
first step of the Metadata-Driven Secure Prompting workflow.

This script creates a LOCAL-ONLY metadata review file. The file is not yet safe
to upload to a GenAI system because it contains the dataset's original column
names.

Students must review the metadata, identify risky columns, and assign safe
aliases before creating metadata for GenAI sharing.
-->

## Role and Objective

Act as an experienced Python data analyst and data-privacy instructor.

Write one complete, executable, and well-commented Python script that loads a CSV dataset into a pandas DataFrame named:

```python
mydata
```

The dataset may be stored:

* on a Windows computer;
* on macOS or Linux;
* in Google Colab;
* in another notebook environment; or
* at a direct public HTTP/HTTPS CSV URL.

The script must inspect the dataset locally and create a metadata-review file for the student.

Do not attempt to make final legal, privacy, or regulatory decisions automatically. The student will review the generated metadata and identify PII, sensitive attributes, quasi-identifiers, confidential fields, and free-text fields.

---

## Configuration

The student should change only this value:

```python
DATA_SOURCE = r"<LOCAL_PATH_OR_DIRECT_CSV_URL>"
```

Examples:

```python
# Windows
DATA_SOURCE = r"C:\Users\Student\Documents\customers.csv"

# macOS or Linux
DATA_SOURCE = "/home/student/data/customers.csv"

# Google Colab
DATA_SOURCE = "/content/customers.csv"

# Direct public CSV URL
DATA_SOURCE = "https://example.org/data/customers.csv"
```

For GitHub, require a direct **Raw** CSV URL.

A GitHub URL containing `/blob/` normally returns an HTML webpage rather than the CSV file. If `/blob/` is detected, stop with a clear message instructing the student to open the file on GitHub, select **Raw**, and copy the Raw URL.

Set the local review-file location automatically:

```python
from pathlib import Path

OUTPUT_FILE = Path.cwd() / "LOCAL_ONLY_mdsp_metadata_review.csv"
```

The student must not be required to configure an output directory.

---

## Required Libraries

Use only:

```python
pandas
pathlib
io
urllib.parse
```

Use additional standard-library modules only when necessary.

Do not require:

* an external GenAI API;
* cloud credentials;
* a remote database;
* a paid service;
* or specialized privacy libraries.

---

## 1. Load the Dataset

The script must:

1. determine whether `DATA_SOURCE` is a local path or an HTTP/HTTPS URL;
2. reject an empty `DATA_SOURCE`;
3. reject unsupported URL schemes;
4. detect a GitHub `/blob/` URL and provide a Raw-URL instruction;
5. load the CSV into a DataFrame named `mydata`;
6. provide clear and sanitized errors for:

   * missing files;
   * inaccessible files;
   * empty CSV files;
   * invalid URLs;
   * connection errors;
   * encoding errors;
   * and malformed CSV files;
7. confirm that the dataset contains at least one column and one data row.

The script must not display the complete local file path or full remote URL in error messages.

---

## 2. Display Local Dataset Information

Print a clear warning first:

```text
LOCAL REVIEW ONLY: Do not copy or upload this output to a GenAI system until the metadata has been reviewed and sanitized.
```

Then display only the following local information.

### Dataset dimensions

Display:

* number of rows;
* number of columns.

### Numbered column list

Display the original column names as a numbered list for local student review.

Example:

```text
1. customer_id
2. age
3. purchase_total
```

Do not display any values from the columns.

### DataFrame information

Display the equivalent of:

```python
mydata.info()
```

This may show:

* column names;
* non-null counts;
* data types;
* approximate memory usage.

### Missing-data summary

Create and print a table containing:

* original column name;
* pandas data type;
* non-null count;
* missing count;
* missing percentage;
* unique-value count.

Do not print the unique values themselves.

### Duplicate-row summary

Display only:

* duplicate-row count;
* duplicate-row percentage.

Do not display duplicate records.

### Numerical summary

For numerical columns only, calculate and display:

* count;
* mean;
* standard deviation;
* 25th percentile;
* median;
* 75th percentile.

Round numerical results to two decimal places.

Do not display:

* minimum values;
* maximum values;
* extreme values;
* outlier records;
* or individual values.

If the dataset has no numerical columns, print a clear message instead of raising an error.

### Categorical-data summary

For non-numerical columns, display only:

* data type;
* non-null count;
* missing count;
* missing percentage;
* unique-value count.

Do not display:

* category labels;
* most frequent values;
* category frequencies;
* rare values;
* free-text values;
* or examples.

---

## 3. Create the Local Metadata-Review File

Create a pandas DataFrame named:

```python
metadata_review
```

It must contain one row for every source column and the following fields:

```text
original_column
default_alias
data_type
non_null_count
missing_count
missing_percentage
unique_count
student_pii_decision
risk_type
recommended_action
safe_to_share
student_notes
```

Populate the fields as follows:

### `original_column`

Store the original column name.

This field is for local review only and must not later be included in metadata shared with GenAI.

### `default_alias`

Automatically create neutral aliases:

```text
column_001
column_002
column_003
```

### `data_type`

Store the pandas data type.

### `non_null_count`

Store the number of non-null records.

### `missing_count`

Store the number of missing records.

### `missing_percentage`

Store the missing percentage rounded to two decimal places.

### `unique_count`

Store the number of distinct non-null values.

Do not store the values themselves.

### `student_pii_decision`

Set the default value to:

```text
Unsure
```

The student must later change it to:

```text
Yes
No
Unsure
```

### `risk_type`

Leave this field blank for student review.

Students may use values such as:

```text
none
direct_identifier
quasi_identifier
sensitive_attribute
confidential
free_text
unknown
```

### `recommended_action`

Set the default value to:

```text
Review
```

Students may later use actions such as:

```text
Keep
Alias
Exclude
Generalize
Aggregate
Review
```

### `safe_to_share`

Set the default value to:

```text
No
```

No column should be considered safe to share until the student has reviewed it.

### `student_notes`

Leave this field blank.

---

## 4. Save the Local Review File

Save `metadata_review` as:

```text
LOCAL_ONLY_mdsp_metadata_review.csv
```

Save it in:

```python
Path.cwd()
```

Use UTF-8 encoding.

If the file already exists, replace it only after printing a clear warning.

The file name must begin with `LOCAL_ONLY_` to remind students that it is not yet approved for GenAI sharing.

---

## 5. Final Student Instructions

After saving the file, print the following instructions:

```text
NEXT MDSP STEP

1. Open LOCAL_ONLY_mdsp_metadata_review.csv locally.
2. Review every original column name.
3. Identify direct identifiers, quasi-identifiers, sensitive attributes,
   confidential fields, and free-text fields.
4. Review or replace each default alias.
5. Select an appropriate recommended action.
6. Change safe_to_share to Yes only for metadata that is safe to disclose.
7. Do not upload this local review file to a GenAI system because it still
   contains the original column names.
8. Create a separate sanitized metadata file before prompting a GenAI model.
```

---

## 6. Mandatory Privacy Rules

The script must never call or display:

```python
mydata.head()
mydata.tail()
mydata.sample()
print(mydata)
display(mydata)
```

The script must never print or save:

* raw rows;
* record samples;
* individual values;
* unique-value lists;
* category labels;
* top or most frequent values;
* free-text contents;
* detected PII values;
* or duplicate records.

The script must not automatically label every column as safe.

The script must not claim:

* that the dataset is anonymous;
* that the dataset contains no PII;
* that the metadata is safe to share;
* that privacy compliance has been achieved;
* or that human review is unnecessary.

---

## 7. Required GenAI Response

Return:

1. one complete executable Python script in a single Python code block;
2. the installation command for pandas;
3. brief instructions explaining how to set `DATA_SOURCE`;
4. brief instructions explaining where the local review file will be saved;
5. a reminder that the review file must not be uploaded to GenAI before sanitization.

The Python script must include:

```python
if __name__ == "__main__":
    main()
```

Do not return:

* pseudocode;
* partial code;
* placeholder functions;
* `pass`;
* TODO comments;
* omitted logic;
* or comments such as “implementation goes here.”

The code must run after the student changes only:

```python
DATA_SOURCE
```
