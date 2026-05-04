# Entity Relationship Diagram - Fuzzy Factory

## Overview
ERD showing the relationships between 6 core tables in the Fuzzy Factory database. The database tracks e-commerce transactions, product information, website analytics, and refunds.

## Diagram

```mermaid
erDiagram
    PRODUCTS ||--o{ ORDERS : "1 to many"
    PRODUCTS ||--o{ ORDER_ITEMS : "1 to many"
    WEBSITE_SESSIONS ||--o{ ORDERS : "1 to many"
    WEBSITE_SESSIONS ||--o{ WEBSITE_PAGEVIEWS : "1 to many"
    ORDERS ||--o{ ORDER_ITEMS : "1 to many"
    ORDERS ||--o{ ORDER_ITEM_REFUNDS : "1 to many"
    ORDER_ITEMS ||--o{ ORDER_ITEM_REFUNDS : "1 to many"

    PRODUCTS {
        int product_id PK
        datetime created_at
        string product_name
    }

    ORDERS {
        int order_id PK
        datetime created_at
        int website_session_id FK
        int user_id FK
        int primary_product_id FK
        int items_purchased
        decimal price_usd
        decimal cogs_usd
    }

    ORDER_ITEMS {
        int order_item_id PK
        datetime created_at
        int order_id FK
        int product_id FK
        binary is_primary_item
        decimal price_usd
        decimal cogs_usd
    }

    ORDER_ITEM_REFUNDS {
        int order_item_refund_id PK
        datetime created_at
        int order_item_id FK
        int order_id FK
        decimal refund_amount_usd
    }

    WEBSITE_SESSIONS {
        int website_session_id PK
        datetime created_at
        int user_id FK
        binary is_repeat_session
        string utm_source
        string utm_campaign
        string utm_content
        string device_type
        string http_referer
    }

    WEBSITE_PAGEVIEWS {
        int website_pageview_id PK
        datetime created_at
        int website_session_id FK
        string pageview_url
    }
```

## Key Relationships

| Relationship | Type | Description |
|---|---|---|
| PRODUCTS → ORDERS | 1 to Many | Each product can be a primary product in multiple orders |
| PRODUCTS → ORDER_ITEMS | 1 to Many | Each product appears in multiple order items |
| WEBSITE_SESSIONS → ORDERS | 1 to Many | Each session can generate multiple orders |
| WEBSITE_SESSIONS → WEBSITE_PAGEVIEWS | 1 to Many | Each session contains multiple page views |
| ORDERS → ORDER_ITEMS | 1 to Many | Each order contains multiple items |
| ORDERS → ORDER_ITEM_REFUNDS | 1 to Many | Each order can have multiple refunds |
| ORDER_ITEMS → ORDER_ITEM_REFUNDS | 1 to Many | Each order item can be refunded |

## Table Descriptions

### PRODUCTS
- Stores product information including ID, creation date, and product name

### ORDERS
- Tracks order transactions with totals (price and COGS), linked to website sessions and products

### ORDER_ITEMS
- Individual items within orders, with per-item pricing and refund tracking

### ORDER_ITEM_REFUNDS
- Refund records for individual order items, linked to both the item and order

### WEBSITE_SESSIONS
- User session tracking including marketing attribution (UTM parameters) and device type

### WEBSITE_PAGEVIEWS
- Page-level analytics, tracking user navigation within sessions</content>
<parameter name="filePath">c:\Users\tsaih\workspace\sample-data\Fuzzy_Factory\erd_diagram.md