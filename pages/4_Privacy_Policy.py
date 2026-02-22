"""Privacy Policy page - Google AdSense compliant."""
import streamlit as st
from utils import render_top_navbar

st.set_page_config(page_title="Privacy Policy | AI Resume Critiquer", page_icon="🔒", layout="centered", initial_sidebar_state="collapsed")
render_top_navbar()

st.title("🔒 Privacy Policy")
st.caption("Last updated: February 2025")
st.markdown("---")

st.markdown("""
## 1. Information We Collect

We may collect information that you provide directly when using AI Resume Critiquer, including:

- **Resume content** — Uploaded files and text are processed by our AI to provide analysis. 
  We do not store your resume content permanently after analysis.
- **Usage data** — We may collect information about how you use our service (e.g., pages visited, features used).
- **Device information** — Such as browser type, operating system, and IP address.

## 2. How We Use Your Information

We use the information we collect to:

- Provide resume analysis and feedback
- Improve our service and user experience
- Respond to your inquiries
- Comply with legal obligations

## 3. Cookies and Similar Technologies

**Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to our website or other websites on the Internet.**

**Google's use of advertising cookies enables it and its partners to serve ads to our users based on their visit to our sites and/or other sites on the Internet.**

We use cookies and similar technologies to:

- Remember your preferences
- Understand how you use our service
- Deliver and measure advertising (where applicable)

## 4. Third-Party Advertising

When we display ads (e.g., through Google AdSense), third-party ad vendors may use cookies and similar technologies to show you relevant ads based on your browsing history. These vendors have their own privacy policies governing how they use your information.

## 5. Opt-Out of Personalized Advertising

You may opt out of personalized advertising by:

- Visiting [Google Ads Settings](https://www.google.com/settings/ads)
- Visiting [www.aboutads.info](https://www.aboutads.info) to opt out of interest-based ads from participating companies

## 6. Data Retention

- Resume content is processed in real time and not stored long-term.
- Analytics and usage data may be retained as needed for service improvement.

## 7. Data Security

We implement appropriate technical and organizational measures to protect your personal information.

## 8. Your Rights

Depending on your location, you may have the right to:

- Access the personal data we hold about you
- Request correction or deletion of your data
- Object to or restrict certain processing
- Data portability

## 9. Children's Privacy

Our service is not intended for users under 13. We do not knowingly collect data from children under 13.

## 10. Changes to This Policy

We may update this Privacy Policy from time to time. We will notify you of material changes by posting the updated policy on this page and updating the "Last updated" date.

## 11. Contact Us

For questions about this Privacy Policy or our data practices, please contact us at:

**Email:** privacy@resumecritiquer.example.com
""")
