<h1>Simple Bulk Mail Sender</h1>
<p>This application is designed to make the process of sending bulk emails as simple and efficient as possible. It allows users to draft and compile emails using pre-defined templates, schedule emails to be sent at a specific time, and prioritize emails based on importance.</p>

<h2>Features</h2>
<ul>
  <li>Draft and compile emails using pre-defined templates</li>
  <li>Schedule emails to be sent at a specific time</li>
  <li>Prioritize emails based on importance</li>
  <li>User authentication and authorization</li>
  <li>Compliance with regulations for sending bulk emails like CAN-SPAM in US and GDPR in EU</li>
</ul>

<h2>Technologies</h2>
<ul>
  <li>Flask web framework</li>
  <li>SQLite database</li>
  <li>Flask-Login library for handling user authentication and authorization</li>
  <li>smtplib library for sending emails via the Gmail SMTP server</li>
  <li>apscheduler library for scheduling the sending of emails</li>
</ul>

<h2>Installation</h2>
<ol>
  <li>Clone the repository
    <pre>git clone https://github.com/[username]/Simple-Bulk-Mail-Sender.git</pre>
  </li>
  <li>Install the required packages
    <pre>pip install -r requirements.txt</pre>
  </li>
  <li>Run the application
    <pre>flask run</pre>
  </li>
</ol>

<h2>Usage</h2>
<ol>
  <li>Register for an account or login if you already have one.</li>
  <li>Create a new email template by navigating to <code>/create</code></li>
  <li>Preview the template before sending by navigating to <code>/preview</code></li>
  <li>Upload a CSV file with recipient information by navigating to <code>/upload</code></li>
  <li>Schedule the sending of emails and/or send immediatelyby navigating to <code>/schedule</code></li>
</ol>

<h2>Contributing</h2>
<p>Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.</p>

<p>Please make sure to update tests as appropriate.</p>

<h2>License</h2>
<p><a href="https://choosealicense.com/licenses/mit/">MIT</a></p>

<h2>Note</h2>
<p>Don't forget to replace gmail_user and gmail_password in config.py with your own credentials.</p>

<p>This code is for demonstration purposes only and should not be used in production environments without proper testing and security measures in place.</p>
