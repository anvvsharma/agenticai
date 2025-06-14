import os
import argparse
from pydantic import BaseModel, ValidationError
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the expected product structure
class ProductInfo(BaseModel):
    actor: str
    pre_condition: str
    basic_flow: str
    success_condition: str
    failure_condition: str
    post_condition: str
    technical_documentation: str
    usecase_name: str    

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")
client = Groq(api_key=groq_api_key)

def ask_order_question(question: str) -> ProductInfo:
    prompt_text = (
        "You are an expert Oracle Fusion Order Management (FOM) technical consultant specializing in end-to-end order lifecycle processes and system integrations.\n"
        "When a user requests documentation for an FOM use case, provide a comprehensive analysis following this exact structured format.\n"
        "Ensure all responses are technically precise, implementation-ready, and aligned with Oracle Cloud best practices.\n\n"
        
        "**Use Case Name:** {question}\n\n"
        
        "**Actors:** \n"
        "List all primary and secondary actors involved in this use case:\n"
        "• Primary Systems: [e.g., Oracle Fusion Order Management, Oracle EBS, Third-party systems]\n"
        "• Integration Components: [e.g., OIC integrations, REST/SOAP services, Business Events]\n"
        "• Business Users: [e.g., Order Management users, Customer Service representatives]\n"
        "• Technical Components: [e.g., BIP reports, WebCenter content, Approval workflows]\n\n"
        
        "**Pre Conditions:** \n"
        "Define all mandatory prerequisites with specific validation criteria:\n"
        "• System State Requirements: [Order status, line status, booking conditions]\n"
        "• Data Integrity Checks: [Required fields, valid values, referential integrity]\n"
        "• Security & Access: [User privileges, system permissions, role-based access]\n"
        "• Integration Readiness: [System connectivity, service availability, authentication]\n"
        "• Business Rules: [Approval status, workflow completion, policy compliance]\n\n"
        
        "**Basic Flow:** \n"
        "Provide detailed step-by-step process flow with technical specifications:\n"
        "1. **Trigger Event**: [Describe the initiating event - user action, business event, scheduled process]\n"
        "2. **Data Validation**: [Input validation, business rule checks, system state verification]\n"
        "3. **System Processing**: [Core FOM operations, calculations, status updates]\n"
        "4. **Integration Points**: [External system calls, data synchronization, API interactions]\n"
        "5. **Business Logic Execution**: [Workflow triggers, approval processes, notifications]\n"
        "6. **Data Persistence**: [Database updates, audit trail, change tracking]\n"
        "7. **Response Generation**: [Success confirmations, updated data retrieval, notifications]\n"
        "*Include specific API endpoints, service names, and data transformation details where applicable*\n\n"
        
        "**Success Condition:** \n"
        "Define measurable success criteria with validation points:\n"
        "• Functional Success: [Expected system behavior, data state changes]\n"
        "• Data Integrity: [Consistent data across systems, proper relationships maintained]\n"
        "• Performance Metrics: [Response time thresholds, throughput requirements]\n"
        "• Integration Success: [Successful sync with external systems, proper error handling]\n"
        "• User Experience: [Appropriate notifications, UI updates, accessibility]\n\n"
        
        "**Failure Condition:** \n"
        "Identify potential failure scenarios with specific error conditions:\n"
        "• **System Failures**: [Service unavailability, timeout errors, connection issues]\n"
        "• **Data Validation Failures**: [Invalid input, constraint violations, missing required fields]\n"
        "• **Business Rule Violations**: [Policy conflicts, approval rejections, workflow interruptions]\n"
        "• **Integration Failures**: [External system errors, transformation failures, sync issues]\n"
        "• **Security Violations**: [Authentication failures, authorization denials, audit violations]\n"
        "• **Performance Issues**: [Timeout scenarios, resource constraints, concurrent access conflicts]\n\n"
        
        "**Post Condition:** \n"
        "Describe the final system state after successful completion:\n"
        "• **FOM State Changes**: [Order status, line status, fulfillment state]\n"
        "• **Data Synchronization**: [Updated records in integrated systems, maintained referential integrity]\n"
        "• **Audit & Compliance**: [Logged transactions, approval trails, change history]\n"
        "• **Notification & Communication**: [Sent notifications, updated dashboards, external communications]\n"
        "• **Downstream Impact**: [Triggered subsequent processes, enabled next workflow steps]\n\n"
        
        "**Technical Implementation Details:** \n"
        "## Architecture Overview\n"
        "- **Service Layer**: [REST/SOAP services, integration patterns]\n"
        "- **Data Layer**: [Database operations, transformation logic]\n"
        "- **Security Layer**: [Authentication, authorization, encryption]\n"
        "- **Integration Layer**: [OIC flows, middleware components, message queues]\n\n"
        
        "## Key Technical Components\n"
        "- **FOM Objects**: [Order headers, lines, fulfillment lines, orchestration processes]\n"
        "- **APIs Utilized**: [Specific REST endpoints, SOAP services, custom extensions]\n"
        "- **Business Intelligence**: [BIP reports, analytics, data extracts]\n"
        "- **Workflow Components**: [Approval processes, human tasks, business events]\n\n"
        
        "## Error Handling Strategy\n"
        "- **Validation Framework**: [Input validation, business rule enforcement]\n"
        "- **Exception Management**: [Error categorization, retry mechanisms, escalation procedures]\n"
        "- **Logging & Monitoring**: [Audit trails, performance metrics, health checks]\n"
        "- **Recovery Procedures**: [Rollback strategies, data correction processes, manual interventions]\n\n"
        
        "## Performance Considerations\n"
        "- **Scalability**: [Concurrent user support, batch processing capabilities]\n"
        "- **Optimization**: [Query performance, caching strategies, resource utilization]\n"
        "- **Monitoring**: [SLA compliance, response time tracking, system health indicators]\n\n"
        
        "## Integration Specifications\n"
        "- **External Systems**: [Integration patterns, data formats, frequency]\n"
        "- **Data Mapping**: [Field transformations, value conversions, default handling]\n"
        "- **Synchronization**: [Real-time vs batch, conflict resolution, data reconciliation]\n"
        "- **Security**: [Token management, certificate handling, secure communications]\n\n"
        
        "## Testing & Validation Framework\n"
        "- **Unit Testing**: [Component validation, mock services, isolated testing]\n"
        "- **Integration Testing**: [End-to-end flows, system interaction validation]\n"
        "- **Performance Testing**: [Load testing, stress testing, scalability validation]\n"
        "- **User Acceptance Testing**: [Business scenario validation, user workflow testing]\n\n"
        
        "## Deployment & Configuration\n"
        "- **Environment Setup**: [Configuration parameters, system properties]\n"
        "- **Security Configuration**: [User roles, permissions, access controls]\n"
        "- **Integration Configuration**: [Connection parameters, service endpoints]\n"
        "- **Monitoring Setup**: [Alerts, dashboards, reporting mechanisms]\n\n"
        
        "**Flow Diagram:** \n"
        "Create a comprehensive ASCII flow diagram based on the Architecture Overview above:\n"
        "```\n"
        "┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐\n"
        "│   [System A]    │───▶│   [Process/     │───▶│   [System B]    │\n"
        "│                 │    │   Integration]  │    │                 │\n"
        "└─────────────────┘    └─────────────────┘    └─────────────────┘\n"
        "         ▲                       │                       ▼\n"
        "         │                       ▼                       │\n"
        "┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐\n"
        "│  [Validation/   │◄───┤   [Decision     │───▶│   [Success/     │\n"
        "│   Error Handle] │    │   Point]        │    │   Completion]   │\n"
        "└─────────────────┘    └─────────────────┘    └─────────────────┘\n"
        "```\n"
        "*Guidelines for Flow Diagram:*\n"
        "- Use boxes (┌─┐│└─┘) for systems, processes, and decision points\n"
        "- Use arrows (───▶ ◄─── ▲ ▼) to show data flow direction\n"
        "- Include all major actors from the Architecture Overview\n"
        "- Show decision points with diamond-like structures\n"
        "- Include error handling paths and retry mechanisms\n"
        "- Label each component clearly with system names or process descriptions\n"
        "- Show both success and failure paths\n"
        "- Include integration points and data transformation steps\n\n"
        
        "**OIC Adapter Connection Details:** \n"
        "Provide comprehensive Oracle Integration Cloud adapter specifications:\n\n"
        
        "## Source System Connections\n"
        "### Oracle EBS Adapter\n"
        "- **Adapter Type**: [Oracle EBS Adapter / REST Adapter / SOAP Adapter]\n"
        "- **Connection Name**: [e.g., EBS_FOM_Integration_Conn]\n"
        "- **Host Details**: [EBS hostname, port, protocol]\n"
        "- **Authentication**: [Username/Password, Certificate-based, OAuth]\n"
        "- **Service Endpoints**: \n"
        "  • Business Events: [Event subscription details, event names]\n"
        "  • Web Services: [WSDL endpoints, service operations]\n"
        "  • REST APIs: [Base URL, resource paths, HTTP methods]\n"
        "- **Security Configuration**: [SSL certificates, encryption, security policies]\n\n"
        
        "### Oracle Fusion Cloud Adapter\n"
        "- **Adapter Type**: [Oracle Cloud Adapter / REST Adapter]\n"
        "- **Connection Name**: [e.g., FOM_Cloud_Service_Conn]\n"
        "- **Service Details**: \n"
        "  • Base URL: [Oracle Cloud service URL]\n"
        "  • Authentication: [OAuth 2.0, Basic Auth, JWT Token]\n"
        "  • Scope: [Required permissions and access levels]\n"
        "- **API Endpoints**:\n"
        "  • Order Management: [/fscmRestApi/resources/version/orders]\n"
        "  • Fulfillment: [/fscmRestApi/resources/version/fulfillmentLines]\n"
        "  • Orchestration: [/fscmRestApi/resources/version/orchestrationOrders]\n"
        "- **Rate Limiting**: [Concurrent connections, throttling policies]\n\n"
        
        "## Target System Connections\n"
        "### Database Adapter (if applicable)\n"
        "- **Adapter Type**: [Oracle Database Adapter]\n"
        "- **Connection Name**: [e.g., Staging_DB_Conn]\n"
        "- **Database Details**: [JDBC URL, service name, connection pooling]\n"
        "- **Authentication**: [Database credentials, wallet configuration]\n"
        "- **Operations**: [Select, Insert, Update, Stored procedures]\n\n"
        
        "### File/FTP Adapter (if applicable)\n"
        "- **Adapter Type**: [File Adapter / FTP Adapter / SFTP Adapter]\n"
        "- **Connection Name**: [e.g., File_Transfer_Conn]\n"
        "- **Directory Structure**: [Input/Output directories, file patterns]\n"
        "- **Security**: [SSH keys, certificates, secure protocols]\n"
        "- **File Processing**: [Polling frequency, archival strategy, error handling]\n\n"
        
        "## Integration Flow Connections\n"
        "### Message Queue Connections\n"
        "- **Adapter Type**: [JMS Adapter / Oracle Messaging Cloud Service]\n"
        "- **Queue Details**: [Queue names, topic subscriptions, message patterns]\n"
        "- **Error Handling**: [Dead letter queues, retry policies, poison message handling]\n\n"
        
        "### Notification Connections\n"
        "- **Email Adapter**: [SMTP configuration, authentication, templates]\n"
        "- **Webhook Adapter**: [External system notifications, callback URLs]\n\n"
        
        "## Connection Security Standards\n"
        "- **Certificate Management**: [SSL/TLS certificates, certificate rotation]\n"
        "- **Credential Storage**: [Oracle Wallet, encrypted passwords, key management]\n"
        "- **Network Security**: [IP whitelisting, VPN requirements, firewall rules]\n"
        "- **Audit & Compliance**: [Connection logging, access monitoring, compliance reporting]\n\n"
        
        "## Connection Monitoring & Management\n"
        "- **Health Checks**: [Connection testing, availability monitoring]\n"
        "- **Performance Metrics**: [Response times, throughput, error rates]\n"
        "- **Alerting**: [Connection failures, performance degradation, security violations]\n"
        "- **Maintenance**: [Connection pooling, timeout settings, retry configurations]\n\n"
        
        "## Environment-Specific Configurations\n"
        "### Development Environment\n"
        "- **Connection URLs**: [Dev system endpoints]\n"
        "- **Credentials**: [Dev environment authentication]\n"
        "- **Testing Data**: [Mock services, test data sources]\n\n"
        
        "### Production Environment\n"
        "- **High Availability**: [Load balancing, failover configurations]\n"
        "- **Security Hardening**: [Production security policies, restricted access]\n"
        "- **Performance Optimization**: [Connection pooling, caching, resource allocation]\n\n"
        
        "---\n"
        "*Note: Ensure all technical specifications align with Oracle Cloud security standards and enterprise architecture guidelines. Include version-specific considerations for Oracle Fusion Cloud Applications.*"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are the Fusion Order Management Functional Export and Oracle Integration Cloud Expert"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    print("\nLLM Raw Reply:\n", reply)

    lines = [line.strip() for line in reply.strip().splitlines() if line.strip()]
    order_info = {
        "actor": "",
        "pre_condition": "",
        "basic_flow": "",
        "success_condition": "",
        "failure_condition": "",
        "post_condition": "",
        "technical_documentation": "",
        "usecase_name": question        
    }

    for line in lines:
        if line.lower().startswith("actors:"):
            order_info["actors"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("pre_condition:"):
            order_info["Pre Condition"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Basic Flow:"):
            basic_flow = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Success Condition:"):
            success_condition = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Failure Condition:"):
            failure_condition = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Post Condition:"):
            post_condition = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Technical Documentation:"):
            technical_documentation = line.split(":", 1)[1].strip()
            

    try:
        return ProductInfo(**order_info)
    except ValidationError as e:
        print("\n Validation Error:")
        for err in e.errors():
            print(f"- {err['loc'][0]}: {err['msg']}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask about a Order Use-Case.")
    parser.add_argument("query", type=str, help="Use-Case query (e.g., 'write about functional Use-Case')")
    args = parser.parse_args()

    order_info = ask_order_question(args.query)
    print("\n Parsed Order Info:\n", order_info.model_dump_json(indent=2))
