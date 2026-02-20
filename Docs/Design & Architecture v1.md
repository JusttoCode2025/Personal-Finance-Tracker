# Software Design Document (SDD)

## 1. Introduction
- **Purpose**: The purpose of this document is to describe the software design and architecture of the FinanceTracker web application. It will explain the system structure component, data flow, and technical decision made durng development.
- **Scope**: **In Scope**: login and signup UI, user sets monthly income, expense category limits, purchase tracking, tracks purchase towards goal, dashboard, and a congratulations page when goal is reached. **Out of Scope**: multi-user account management, full authentication, muliti-user account management and banking integration
- **Definitions and Acronyms**: UI – User Interface; API – Application Programming Interface; DB – Database

- **References**: https://gist.github.com/iamhenry/2dbabd0d59051eae360d8cfa6a2782bd

---

## 2. System Overview
- **System Description**: FinanceTracker is a Flask-based web application that allows users to manage budget limits and track spending by category in order to reach a major goal
- **Design Goals**: Maintainability and simplicity
- **Architecture Summary**: Flask 
- **System Context Diagram**:
  - *Use Mermaid diagram here.*
  - Example placeholder:
    ```mermaid
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/25fb445c-bde7-42e5-aca8-1aa42288c59d" />

    ```
---

## 3. Architectural Design
- **System Architecture Diagram**:
  - <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/c7ced76c-080e-4ce0-8004-332c3adf1ad7" />
- **Component Breakdown**:
  - - Html, Java, and CSS: Displays system UI, sends a request, and updates data
  - - Flask: Routing and validation
    - Database: Stores limits and purchases
- **Technology Stack**: Python, Flask, HTML, CSS, JavaScript, SQLite, Gunicorn (deployment), and Render (hosting)

- **Data Flow and Control Flow**:
  - <img width="700" height="518" alt="image" src="https://github.com/user-attachments/assets/d91c038a-601e-4c36-a450-829c613974aa" />


---

## 4. Detailed Design
For each module/component:

### Budget Module
- **Responsibilities**: Set limits, add purchases, and calculate remaining balances
- **Interfaces/APIs**:
  - Inputs: category, amount and limit amount.
  - Outputs: Json warning or validation and updated balances
  - Error Handling: Invalid inputs are rejected and if there is missing info it is rejected
- **Data Structures**: spending limits and purchase history
- **Algorithms/Logic**: [Design patterns or important logic.]
- **State Management**: [How is state handled?]

---

## 5. Database Design
- **ER Diagram / Schema Diagram**:
  - *Use Mermaid ER diagram here.*
- **Tables/Collections**: [Define each with fields and constraints.]
- **Relationships**: [Describe relationships between entities.]
- **Migration Strategy**: [If applicable.]

---

## 6. External Interfaces
- **User Interface**: Login, budget, dashboard, about and contact page.
- **External APIs**: [Integrations and dependencies.]
- **Hardware Interfaces**: [If any.]
- **Network Protocols/Communication**:
  - [REST, GraphQL, gRPC, WebSockets, etc.]

---

## 7. Security Considerations
- **Authorization**: Only the UI will be used 
- **Data Protection**: NA
- **Compliance**: [GDPR, HIPAA, etc.]
- **Threat Model**:
  - *Use Mermaid diagram here if helpful.*

---

## 8. Performance and Scalability
- **Expected Load**: [Requests per second, data volume.]
- **Caching Strategy**: [Describe caches used.]
- **Database Optimization**: [Indexes, partitioning.]
- **Scaling Strategy**: [Vertical/horizontal.]

---

## 9. Deployment Architecture
- **Environments**: [Dev, staging, production.]
- **CI/CD Pipeline**: [Tools and stages.]
- **Infrastructure Diagram**:
  - *Use Mermaid diagram here.*
- **Cloud/Hosting**: Render
- **Containerization/Orchestration**: [Docker, Kubernetes.]

---

## 10. Testing Strategy
- **Unit Testing**: [Tools, coverage goals.]
- **Integration Testing**: [Approach and tools.]
- **End-to-End Testing**: [Scope and tools.]
- **Quality Metrics**: [Code coverage, linting, etc.]

---

## 11. Appendices
- **Diagrams**: [All referenced diagrams.]
- **Glossary**: [Terms and definitions.]
- **Change History**:
  - [Version, Date, Author, Changes]

