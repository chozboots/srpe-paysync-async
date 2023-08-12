# SRPE - PaySync (Quart Edition)

> **Note:** This README is currently in a drafting phase and may be subject to changes. While efforts have been made to ensure accuracy, there might be discrepancies. Always refer to the actual code or configuration files for the most up-to-date information.

An asynchronous version of SRPE PaySync, rebuilt with Quart to use the Stripe API for better scalability and adaptability.

## Project Goals:

### User Dashboard
- **Payment Process Monitoring**: Inform users about their payment stages, especially during long micro-deposit phases using `setup_intent` webhooks from Stripe.
  
- **Payment Method Management**: Let users switch payment methods. This uses links to a Stripe-hosted payment modification page, reducing compliance concerns.
  
- **Billing History Access**: Give users an easier way to see their billing history.
  
- **Payment Status Alerts**: Notify users if a payment method is declined or if their balance is empty.

### Process Efficiency
- Handle scenarios like mass member sign-up events.
  
- Use Quart's compatibility with `asyncio` for task management, timers, message brokering, and memory storage.
  
- Set up a dedicated email server on a separate Heroku dyno, probably using the synchronous API from SendGrid.
  
- Use CloudAMQP, with pika as a possibility, for message brokering. Consider adding multi-threading for the email server in the future.
  
- Implement rate-limiting with Redis, especially with the new Bootstrap/HTML/JavaScript UI.

### Code Refinement
- Make the code easier to read and organized.
  
- Introduce error handlers for database, Stripe, and Quart issues.
  
- Implement multi-level logging for local development and ensure data privacy in production.

### Security
- Increase security measures for PII.
  
- Introduce bcrypt for password hashing for the new dashboard.
  
- Use JWT for secure sessions in the dashboard.

### Adaptability Considerations
- Evaluate if the asynchronous setup improves efficiency; if not, consider a Flask fallback.
  
- Adjust the UI elements and logging based on the environment.

## Setup & Deployment

For local setups, refer to the `develop` branch. While waiting for updates to the main branch, use the `develop` branch as a template for your version. Make sure to:

- Set up the `app.run` configurations correctly.
  
- Ensure sensitive files are excluded from version control (check .gitignore and .dockerignore).
  
- Set up your Postgres database, Redis instance, and CloudAMQP. Heroku add-ons can be used for these services.

If you're deploying a modified version, check the LICENSE for compliance.

## Docker

You can use the Docker and `docker-compose.yml` files for building the application locally. If you're deploying on Heroku, you can either use Heroku Containers or align your app with Heroku's environment settings.

## Configuration Variables

For security, always use test keys when testing. Here's a breakdown of required configuration variables:

### Stripe
- **STRIPE_SECRET_KEY**: Needed for most Stripe operations.
  
- **WEBHOOK_SIGNING_SECRET**: For Stripe webhook events.

### SendGrid, CloudAMQP, and Postgres

- **SENDGRID_API_KEY**: For the email service.
  
- **CLOUDAMQP_APIKEY**: For CloudAMQP sessions.
  
- **DATABASE_URL**: For connecting to the Postgres database using the UnionDatabase class.

### Quart and S3 Bucket

- **JWT_SECRET_KEY**: For JWT sessions.
  
- **BUCKETEER_AWS_SECRET_ACCESS_KEY**
- **BUCKETEER_AWS_ACCESS_KEY_ID**
- **BUCKETEER_AWS_REGION**
- **BUCKETEER_BUCKET_NAME**: All for accessing the S3 bucket via the UnionStorage class.

## Path Configurations

Set paths for scripts, bucket management, and log settings. The LOGGER_ENV is especially important for controlling production logs.