# Google Cloud Setup for Debris AI

This document outlines the steps to set up the necessary Google Cloud services for the Debris AI backend.

## 1. Project Setup

1.  **Create a new Google Cloud Project:** If you don't have one already, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable Billing:** Ensure that billing is enabled for your project.

## 2. Enable APIs

Enable the following APIs for your project:

*   **Cloud Run API:** To deploy the backend service.
*   **Vertex AI API:** To use Gemini for image analysis and chat.

You can enable these APIs via the Cloud Console or by using the `gcloud` CLI:

```bash
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

## 3. IAM Permissions

The Cloud Run service needs permissions to access Vertex AI. By default, the service uses the Compute Engine default service account. For a more secure setup, create a dedicated service account.

1.  **Create a Service Account:**

    ```bash
    gcloud iam service-accounts create debris-ai-sa --display-name "Debris AI Service Account"
    ```

2.  **Grant Vertex AI User Role:**

    ```bash
    gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> \
        --member="serviceAccount:debris-ai-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com" \
        --role="roles/aiplatform.user"
    ```

3.  **Deploy Cloud Run with the Service Account:**

    When deploying your Cloud Run service, specify the service account:

    ```bash
    gcloud run deploy debris-ai-backend \
        --source . \
        --platform managed \
        --region <YOUR_REGION> \
        --allow-unauthenticated \
        --service-account debris-ai-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com
    ```

## 4. Environment Variables

When deploying the Cloud Run service, you will need to set the environment variables for your Google Cloud project, region, and Confluent Cloud credentials. See the `confluent_setup.md` file for more details.
