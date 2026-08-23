# Industrial Product Intelligence

## Overview

Industrial Product Intelligence is a configurable product-enrichment pipeline that transforms minimal and fragmented industrial catalogue information into structured, validated, searchable and delivery-ready product intelligence.

The system is designed to separate product enrichment from final catalogue delivery. Instead of relying on static output screens, the pipeline processes catalogue records through identity resolution, attribute enrichment, normalization, taxonomy resolution, controlled vocabulary matching, evidence generation and delivery mapping.

## Problem

Industrial product catalogues frequently contain incomplete or inconsistent information such as:

* Manufacturer part number
* Short product description
* Brand or manufacturer information
* Incomplete attributes
* Inconsistent units and terminology

This makes catalogue standardization, search and downstream commerce operations difficult.

## Solution

The system transforms the available product information through a controlled enrichment pipeline:

```text
Raw Catalogue Input
        ↓
Identity Resolution
        ↓
Attribute Intelligence
        ↓
Normalization
        ↓
Taxonomy / Product Classification
        ↓
Company-Specific LOV Resolution
        ↓
Evidence + Confidence
        ↓
Validation
        ↓
Delivery Adapter
        ↓
252-Field Catalogue Output
```

## Key Features

* Product identity resolution
* Brand and manufacturer resolution
* Structured attribute extraction
* Attribute normalization
* Product classification and taxonomy handling
* Evidence-aware enrichment
* Confidence information
* Company-specific controlled vocabulary / LOV support
* Searchable enriched catalogue
* Evaluator dataset processing
* Delivery-schema validation
* 252-field delivery output
* CSV download
* Streamlit-based inspection interface

## Company-Specific LOV

The enrichment engine is configuration-driven rather than dependent on one fixed company vocabulary.

An organization can provide its own controlled vocabulary / LOV. The same enrichment architecture can then resolve product information according to that organization's approved values and rules.

Conceptually:

```text
Company A LOV → Same Enrichment Engine → Company A Output

Company B LOV → Same Enrichment Engine → Company B Output
```

This allows the solution to be adapted to different enterprise catalogues without rebuilding the complete enrichment pipeline.

## Dynamic Processing

The prototype is not based solely on hard-coded demonstration screens.

Catalogue data is processed through the backend enrichment pipeline and converted into output records. The prototype was also tested using evaluator-provided data to verify that the workflow can operate on data outside the primary demonstration dataset.

## Delivery

The system maps enriched internal records into the required delivery structure and supports a 252-field catalogue output.

The delivery layer is intentionally separated from the enrichment layer so that the enrichment logic can be reused while the final output schema can be adapted for downstream systems.

## Prototype

The Streamlit application provides:

1. Pipeline architecture view
2. Product search
3. Structured product inspection
4. Company LOV inspection
5. Evaluation / validation
6. Delivery preview
7. 252-field schema inspection
8. Final CSV download

## Technology

* Python
* Pandas
* Streamlit
* CSV / Excel data processing
* Modular Python enrichment components
* Configuration-driven controlled vocabulary / LOV
* Git / GitHub

## Project Structure

```text
src/
    pipeline.py
    catalogue.py
    normalizer.py
    final_output.py
    attribute_evidence.py
    ...

scripts/
    run_demo.py
    run_batch3.py
    run_batch4.py
    run_batch5.py

data/
    raw/
    demo/
    output/

app.py
requirements.txt
README.md
```

## Running the Prototype

Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit prototype:

```bash
streamlit run app.py
```

## Running the Enrichment Pipeline

The project contains separate processing stages for catalogue enrichment and final output generation.

The exact scripts included in the repository can be executed from the project root.

The final enrichment stage produces a search-ready product output, while the delivery layer maps the enriched information into the required catalogue schema.

## Validation Philosophy

The system is designed to avoid treating generated text as automatically correct.

Values can be accompanied by evidence and confidence information, while unresolved information can remain unresolved rather than being silently fabricated.

Company-controlled vocabularies can further constrain acceptable values.

## Scalability

The architecture separates:

* Input processing
* Enrichment
* Normalization
* Classification
* Governance
* Validation
* Delivery

This separation allows the same enrichment engine to be extended to larger catalogues, additional manufacturers, additional document formats and continuously updated product data.

## Future Development

Future production deployment could extend the prototype with:

* Manufacturer-document ingestion
* Official manufacturer website/document retrieval
* Incremental catalogue updates
* Queue-based large-scale processing
* Enterprise PIM / ERP integration
* Human-review queues for low-confidence records
* Expanded taxonomy coverage
* Automated monitoring and data-quality reporting

## Hackathon Context

This project was developed as an MVP/POC for an industrial product data enrichment challenge, with emphasis on dynamic processing, controlled enrichment, explainability, company-specific vocabulary support and delivery-ready catalogue output.
