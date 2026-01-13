# KidsPlaza Sales Reconciliation Pipeline

KidsPlaza Sales Reconciliation Pipeline powers the internal ETL process for consolidating, validating, and standardizing retail sales data at KidsPlaza.

This pipeline is designed to ingest sales data from **multiple heterogeneous sources** such as local files (CSV, Excel, Parquet, JSON), databases, and data warehouses, transforming them into a unified and analysis-ready format within a centralized data environment (e.g. Google BigQuery).

Its primary purpose is to support **descriptive analysis**, reconciliation, and reporting for retail sales performance across channels, time periods, and promotional programs.

---

## Use Cases

- Sales reconciliation between:
  - Offline systems vs online platforms
  - Raw operational exports vs reporting dashboards
- Descriptive analysis of:
  - Sales volume and revenue trends
  - Channel and store-level performance
  - Promotion and campaign effectiveness
- Data quality checks and anomaly detection in retail sales flows

---

## Ownership

This repository is maintained by the **Data & Analytics / Digital Team at KidsPlaza**.

For questions, access requests, or contributions, please contact:

- **Internal:** quang.nn@kidsplaza.vn  
- **External:** nhatquang.nguyen.129@gmail.com  
- Or reach out via the internal Slack channel **#data-engineering**

---

## Disclaimer

This project is intended for **internal use only**.

It contains custom business logic tailored specifically to KidsPlaza’s retail data structures, sales processes, reconciliation rules, and naming conventions.  
Do **not** reuse, replicate, or adapt this codebase outside of KidsPlaza without prior approval.

---

## License

All content and source code in this repository is **proprietary to KidsPlaza**.

Redistribution, publication, or open-sourcing of any part of this project is strictly prohibited without explicit written consent from the company.

---

## AI-Assisted Development

This repository includes code, documentation, and architectural guidance that has been **partially developed or enhanced using AI tools** (e.g. GitHub Copilot, ChatGPT by OpenAI), under the supervision of the development team.

All AI-assisted output has been reviewed, validated, and adapted to meet KidsPlaza’s internal engineering and production standards.