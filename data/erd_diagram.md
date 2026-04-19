```mermaid
erDiagram
    website_sessions ||--o{ website_pageviews : "contains"
    website_sessions ||--o{ orders : "leads to"
    orders ||--o{ order_items : "contains"
    order_items ||--|| products : "references"
    orders ||--|| products : "primary product"
    order_items ||--o| order_item_refunds : "has refund"

    website_sessions {
        int website_session_id PK
        datetime created_at
        int user_id
        int is_repeat_session
        string utm_source
        string utm_campaign
        string utm_content
        string device_type
        string http_referer
    }

    website_pageviews {
        int website_pageview_id PK
        datetime created_at
        int website_session_id FK
        string pageview_url
    }

    orders {
        int order_id PK
        datetime created_at
        int website_session_id FK
        int user_id
        int primary_product_id FK
        int items_purchased
        float price_usd
        float cogs_usd
    }

    order_items {
        int order_item_id PK
        datetime created_at
        int order_id FK
        int product_id FK
        int is_primary_item
        float price_usd
        float cogs_usd
    }

    products {
        int product_id PK
        datetime created_at
        string product_name
    }

    order_item_refunds {
        int order_item_refund_id PK
        datetime created_at
        int order_item_id FK
        int order_id FK
        float refund_amount_usd
    }
```</content>
<parameter name="filePath">c:\Users\tsaih\workspace\sample-data\Fuzzy_Factory\erd_diagram.md