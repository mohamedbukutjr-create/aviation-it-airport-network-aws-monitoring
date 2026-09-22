from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table, TableStyle
from reportlab.lib.enums import TA_CENTER

outdir=Path('/root/.hermes/cache/documents/aviation-it-portfolio')
repo=Path('/root/aviation-it-portfolio')
outdir.mkdir(parents=True, exist_ok=True)
styles=getSampleStyleSheet()
for name in ['TitleNavy','H1N','H2N','BodyX','SmallX','BulletX','CodeBlock']:
    if name in styles: del styles.byName[name]
styles.add(ParagraphStyle(name='TitleNavy', parent=styles['Title'], fontSize=22, leading=26, alignment=TA_CENTER, textColor=colors.HexColor('#003A70'), spaceAfter=16))
styles.add(ParagraphStyle(name='H1N', parent=styles['Heading1'], fontSize=16, leading=19, textColor=colors.HexColor('#003A70'), spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name='H2N', parent=styles['Heading2'], fontSize=12.5, leading=15, textColor=colors.HexColor('#1F2937'), spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyX', parent=styles['Normal'], fontSize=9.5, leading=12.5, spaceAfter=6))
styles.add(ParagraphStyle(name='SmallX', parent=styles['Normal'], fontSize=8.2, leading=10.2, textColor=colors.HexColor('#374151')))
styles.add(ParagraphStyle(name='BulletX', parent=styles['BodyX'], leftIndent=14, firstLineIndent=-8))
styles.add(ParagraphStyle(name='CodeBlock', parent=styles['Code'], fontName='Courier', fontSize=6.7, leading=7.8, backColor=colors.HexColor('#F3F4F6')))

def tbl(data, widths=None):
    t=Table([[Paragraph(str(c), styles['SmallX']) for c in r] for r in data], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#003A70')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),0.25,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#F8FAFC')),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5)]))
    return t

def footer(title):
    def f(canvas, doc):
        canvas.saveState(); canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#6B7280'))
        canvas.drawString(.55*inch,.35*inch,title[:70]); canvas.drawRightString(7.95*inch,.35*inch,f'Page {doc.page}')
        canvas.restoreState()
    return f

def P(story,t,s='BodyX'): story.append(Paragraph(t, styles[s]))
def B(story,items):
    for i in items: P(story,'• '+i,'BulletX')
def C(story,t): story.append(Preformatted(t.strip(), styles['CodeBlock'])); story.append(Spacer(1,6))
def T(story,data,widths=None): story.append(tbl(data,widths)); story.append(Spacer(1,7))

def build_network():
    title='EVE-NG Airport VLAN Network Project Guide'
    story=[]
    P(story,title,'TitleNavy')
    P(story,'Expanded step-by-step aviation IT networking lab for GitHub portfolio, NOC/network support interviews, and hands-on EVE-NG practice.','SmallX')
    P(story,'This project simulates the kind of segmented network that supports airline airport operations: check-in counters, gate systems, baggage scanners/printers, SOCC/operations users, IT management, guest Wi-Fi, and internal application servers.','BodyX')
    P(story,'1. Business Scenario','H1N')
    P(story,'A regional airline expanding at Toronto Pearson needs a secure airport operations network. Sensitive airline systems must be separated from guest Wi-Fi, baggage devices must reliably reach baggage services, and IT administrators need secure SSH access to network devices. The design must be easy to troubleshoot during flight disruptions.','BodyX')
    P(story,'2. Skills Demonstrated','H1N')
    B(story,['VLAN design and network segmentation','802.1Q trunking','Router-on-a-stick inter-VLAN routing','DHCP scopes per airport department','Internal DNS design','ACL security policy for guest and baggage networks','SSH management hardening','Baggage scanner/printer troubleshooting','ITIL-style incident documentation','GitHub-ready technical documentation'])
    P(story,'3. Lab Topology Design','H1N')
    P(story,'The design uses one edge router and one Layer 2 switch. The router performs inter-VLAN routing through subinterfaces, while the switch places each airport endpoint into the correct access VLAN. This is a strong beginner-to-intermediate EVE-NG design because it shows the same segmentation logic used in real airports without requiring many expensive virtual images.','BodyX')
    P(story,'Physical Topology Diagram','H2N')
    C(story,'''
                                  R1-AIRPORT-EDGE
                       Router-on-a-stick / DHCP / ACL firewall
                                          |
                                  G0/0 802.1Q trunk
                                          |
                                      SW1-CORE
                               Layer 2 airport access switch
       -----------------------------------------------------------------
       |          |          |           |           |          |       |
   VLAN 10    VLAN 20    VLAN 30     VLAN 40     VLAN 50    VLAN 60 VLAN 70
  CHECK-IN     GATES     BAGGAGE       OPS       IT-MGMT     GUEST  SERVERS
       |          |       |     |        |           |          |       |
 CHECKIN-PC  GATE-PC  SCANNER PRINTER  OPS-PC    IT-ADMIN  GUEST  DNS/APPS
''')
    P(story,'Logical VLAN Topology','H2N')
    C(story,'''
R1 G0/0.10  -> VLAN 10 CHECKIN      -> 10.10.10.1/24
R1 G0/0.20  -> VLAN 20 GATE         -> 10.10.20.1/24
R1 G0/0.30  -> VLAN 30 BAGGAGE      -> 10.10.30.1/24
R1 G0/0.40  -> VLAN 40 AIRPORT_OPS  -> 10.10.40.1/24
R1 G0/0.50  -> VLAN 50 IT_MGMT      -> 10.10.50.1/24
R1 G0/0.60  -> VLAN 60 GUEST_WIFI   -> 10.10.60.1/24
R1 G0/0.70  -> VLAN 70 SERVERS      -> 10.10.70.1/24
''')
    P(story,'4. EVE-NG Node and Cable Plan','H1N')
    T(story,[['Node','Interface','Connects To','Purpose'],['R1-AIRPORT-EDGE','G0/0','SW1 G0/0','802.1Q trunk'],['SW1-CORE','G0/1','SRV-DNS-DHCP','Server VLAN 70'],['SW1-CORE','G0/2','CHECKIN-PC1','VLAN 10'],['SW1-CORE','G0/3','GATE-PC1','VLAN 20'],['SW1-CORE','G1/0','BAG-SCANNER1','VLAN 30'],['SW1-CORE','G1/1','BAG-PRINTER1','VLAN 30'],['SW1-CORE','G1/2','OPS-PC1','VLAN 40'],['SW1-CORE','G1/3','IT-ADMIN-PC','VLAN 50'],['SW1-CORE','G2/0','GUEST-LAPTOP','VLAN 60']], [1.2*inch,0.8*inch,1.6*inch,2.2*inch])
    P(story,'4. IP Addressing Plan','H1N')
    T(story,[['VLAN','Name','Subnet','Gateway','Purpose'],['10','CHECKIN','10.10.10.0/24','10.10.10.1','Check-in PCs and bag tag systems'],['20','GATE','10.10.20.0/24','10.10.20.1','Gate/boarding devices'],['30','BAGGAGE','10.10.30.0/24','10.10.30.1','Baggage scanners and printers'],['40','AIRPORT_OPS','10.10.40.0/24','10.10.40.1','Ops/SOCC workstations'],['50','IT_MGMT','10.10.50.0/24','10.10.50.1','Admin and management'],['60','GUEST_WIFI','10.10.60.0/24','10.10.60.1','Guest Wi-Fi'],['70','SERVERS','10.10.70.0/24','10.10.70.1','DNS/apps/monitoring']], [0.55*inch,1.0*inch,1.25*inch,1.05*inch,2.05*inch])
    P(story,'5. Build Steps in EVE-NG','H1N')
    B(story,['Create a new EVE-NG lab named Aviation-IT-Airport-Network.','Add Cisco IOSv/CSR1000v router and IOSvL2/IOL L2 switch.','Add VPCS nodes for each airport endpoint.','Cable the trunk and access links using the table above.','Start R1 and SW1 first, then endpoint nodes.','Paste the switch configuration into SW1, then save.','Paste the router configuration into R1, then save.','On each VPCS client, run ip dhcp and show ip.','Run verification commands and capture screenshots for GitHub.'])
    P(story,'6. Switch Configuration','H1N')
    C(story,(repo/'PROJECT-1-EVE-NG-Airport-Network/configs/SW1-CORE.cfg').read_text())
    P(story,'7. Router Configuration','H1N')
    C(story,(repo/'PROJECT-1-EVE-NG-Airport-Network/configs/R1-AIRPORT-EDGE.cfg').read_text())
    P(story,'8. Verification Commands','H1N')
    C(story,'''show vlan brief
show interfaces trunk
show ip interface brief
show ip dhcp binding
show access-lists
show mac address-table dynamic
ping 10.10.70.10
ssh -l admin 10.10.50.2''')
    P(story,'9. Test Matrix','H1N')
    T(story,[['Test','Expected Result','If it fails, check'],['Guest to 10.10.70.10','Blocked','ACL on G0/0.60 inbound'],['Baggage to 10.10.70.30','Allowed','BAGGAGE-IN ACL, DNS, server IP'],['Check-in to DCS 10.10.70.20','Allowed','CHECKIN-IN ACL and DNS'],['IT admin to SW1 SSH','Allowed','VLAN50, SSH keys, VTY lines'],['Wrong VLAN endpoint','DHCP wrong subnet or no access','Switchport access VLAN and trunk allowed VLANs']], [1.55*inch,1.75*inch,2.6*inch])
    P(story,'10. Baggage Scanner and Printer Runbook','H1N')
    C(story,(repo/'PROJECT-1-EVE-NG-Airport-Network/runbooks/baggage-scanner-printer-troubleshooting.md').read_text())
    P(story,'11. Mock Incident Tickets','H1N')
    C(story,(repo/'PROJECT-1-EVE-NG-Airport-Network/incidents/mock-incident-tickets.md').read_text())
    P(story,'12. GitHub Evidence Checklist','H1N')
    B(story,['EVE-NG topology screenshot','show vlan brief','show interfaces trunk','show ip dhcp binding','show access-lists with hit counters','Successful internal ping tests','Failed guest-to-internal ping test','Completed incident tickets and runbook','Short LinkedIn post explaining the project'])
    P(story,'13. Interview Explanation','H1N')
    P(story,'In this project I designed an airport-style network using VLAN segmentation to separate check-in, gate, baggage, operations, management, guest Wi-Fi and server networks. I used router-on-a-stick for inter-VLAN routing, DHCP for endpoint addressing, DNS design for airline applications, ACLs to block guest access to internal systems, and runbooks to troubleshoot baggage scanner and printer failures.','BodyX')
    path=outdir/'EVE-NG_Airport_VLAN_Network_Project_Guide.pdf'
    doc=SimpleDocTemplate(str(path),pagesize=letter,rightMargin=.55*inch,leftMargin=.55*inch,topMargin=.55*inch,bottomMargin=.55*inch)
    doc.build(story,onFirstPage=footer(title),onLaterPages=footer(title)); return path

def build_aws():
    title='AWS Airline Cloud Monitoring Project Guide'
    story=[]
    P(story,title,'TitleNavy')
    P(story,'Expanded step-by-step AWS cloud monitoring lab for aviation IT, NOC, cloud support, and GitHub portfolio preparation.','SmallX')
    P(story,'This project simulates cloud monitoring for a mock airline operations application supporting check-in, baggage events and operations dashboards. It uses Terraform to define infrastructure and CloudWatch/SNS to model production monitoring and incident response.','BodyX')
    P(story,'1. Business Scenario','H1N')
    P(story,'The airport operations team uses a cloud-hosted dashboard to monitor airline operations. IT must deploy secure cloud networking, monitor the app, alert on failures, and document incidents clearly for NOC/cloud support handoff.','BodyX')
    P(story,'2. Skills Demonstrated','H1N')
    B(story,['AWS VPC and subnet design','Security groups and least-privilege thinking','Terraform Infrastructure as Code','CloudWatch dashboard and alarms','SNS alerting workflow','EC2 app server readiness','Incident runbooks and mock tickets','Cost-control and destroy workflow'])
    P(story,'3. Architecture','H1N')
    T(story,[['Component','Purpose'],['VPC 10.20.0.0/16','Cloud network boundary'],['Public subnet 10.20.10.0/24','Optional web app subnet'],['Private ops subnet 10.20.20.0/24','Private operations placeholder'],['Internet Gateway','Public subnet internet path'],['Security Group','HTTP/SSH limited to admin CIDR'],['CloudWatch Log Group','Application log collection placeholder'],['CloudWatch Dashboard','NOC monitoring view'],['SNS Topic','Alert notification path'],['Terraform','Repeatable build/destroy']], [2.0*inch,3.8*inch])
    P(story,'4. Prerequisites','H1N')
    B(story,['AWS account and budget alert','AWS CLI configured','Terraform installed','IAM permission for VPC, EC2, CloudWatch and SNS','Your public IP address for allowed_admin_cidr','GitHub repository created or local repo ready'])
    P(story,'5. Safety and Cost Control','H1N')
    B(story,['Keep create_ec2=false for the first deployment.','Use ca-central-1 if you want a Canada region.','Never commit tfvars, credentials, access keys or state files.','Restrict SSH/HTTP to your IP /32.','Run terraform destroy after screenshots/testing.'])
    P(story,'6. Terraform Files','H1N')
    P(story,'main.tf','H2N'); C(story,(repo/'PROJECT-2-AWS-Airline-Cloud-Monitoring/terraform/main.tf').read_text())
    P(story,'variables.tf','H2N'); C(story,(repo/'PROJECT-2-AWS-Airline-Cloud-Monitoring/terraform/variables.tf').read_text())
    P(story,'outputs.tf','H2N'); C(story,(repo/'PROJECT-2-AWS-Airline-Cloud-Monitoring/terraform/outputs.tf').read_text())
    P(story,'user_data.sh','H2N'); C(story,(repo/'PROJECT-2-AWS-Airline-Cloud-Monitoring/terraform/user_data.sh').read_text())
    P(story,'7. Step-by-Step Deployment','H1N')
    C(story,'''aws configure
aws sts get-caller-identity
cd PROJECT-2-AWS-Airline-Cloud-Monitoring/terraform
terraform init
terraform validate
terraform plan
terraform apply
terraform output''')
    P(story,'8. Optional EC2 Deployment','H1N')
    P(story,'The Terraform defaults keep EC2 disabled so you can review the network and monitoring shell safely. To deploy EC2, find a valid Amazon Linux 2023 AMI in ca-central-1, set create_ec2=true and ami_id="ami-xxxxxxxx" in terraform.tfvars, then run terraform plan and apply again.','BodyX')
    P(story,'9. AWS Verification Commands','H1N')
    C(story,'''aws ec2 describe-vpcs --filters Name=tag:Name,Values=aviation-it-vpc
aws ec2 describe-subnets --filters Name=vpc-id,Values=<vpc-id>
aws sns list-topics
aws cloudwatch list-dashboards
aws cloudwatch describe-alarms
terraform output''')
    P(story,'10. Cloud Monitoring Runbook','H1N')
    C(story,(repo/'PROJECT-2-AWS-Airline-Cloud-Monitoring/runbooks/cloud-monitoring-runbook.md').read_text())
    P(story,'11. Mock Cloud Incident Tickets','H1N')
    C(story,(repo/'PROJECT-2-AWS-Airline-Cloud-Monitoring/incidents/mock-cloud-incident-tickets.md').read_text())
    P(story,'12. GitHub Evidence Checklist','H1N')
    B(story,['terraform init/validate screenshot','terraform plan screenshot','AWS VPC screenshot','Subnets and route table screenshot','CloudWatch dashboard screenshot','CloudWatch alarm screenshot if EC2 enabled','SNS topic screenshot','Incident tickets and runbook','terraform destroy screenshot'])
    P(story,'13. Resume and Interview Explanation','H1N')
    P(story,'Resume bullet: Built an AWS cloud monitoring lab for a mock airline operations application using VPC networking, EC2-ready Terraform, IAM concepts, CloudWatch dashboards/alarms, SNS alerting, security groups, incident tickets and operational runbooks.','BodyX')
    P(story,'Interview explanation: I used Terraform to define a repeatable AWS aviation IT monitoring environment. The design includes a VPC, subnets, internet gateway, security group, optional EC2 web app, CloudWatch dashboard/alarm and SNS topic. I documented how a NOC/cloud support analyst would respond to high CPU, app unreachable, SNS failure and SSH blocked incidents.','BodyX')
    P(story,'14. Cleanup','H1N')
    C(story,'terraform destroy')
    path=outdir/'AWS_Airline_Cloud_Monitoring_Project_Guide.pdf'
    doc=SimpleDocTemplate(str(path),pagesize=letter,rightMargin=.55*inch,leftMargin=.55*inch,topMargin=.55*inch,bottomMargin=.55*inch)
    doc.build(story,onFirstPage=footer(title),onLaterPages=footer(title)); return path

print(build_network())
print(build_aws())
