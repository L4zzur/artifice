import "./config";

import {
  generatePasswordApiV1PasswordGeneratePost,
  analyzePasswordApiV1PasswordAnalyzePost,
} from "./generated/sdk.gen";
import type {
  PasswordGenerateRequest,
  PasswordGenerateResponse,
  PasswordAnalyzeRequest,
  PasswordAnalyzeResponse,
} from "./generated/types.gen";

/**
 * Generate password with strength analysis
 *
 * @param params - Password generation parameters
 * @returns Promise<PasswordGenerateResponse> - Generated password data
 * @throws Error if generation fails
 */
export async function generatePassword(
  params: PasswordGenerateRequest,
): Promise<PasswordGenerateResponse> {
  try {
    const response = await generatePasswordApiV1PasswordGeneratePost({
      body: params,
    });

    if (response.error) {
      handleApiError(response.error);
    }

    if (!response.data) {
      throw new Error("No data received from server");
    }

    return response.data;
  } catch (err) {
    throw err;
  }
}

/**
 * Analyze password strength
 *
 * @param params - Password analysis parameters
 * @returns Promise<PasswordAnalyzeResponse> - Analyzed password data
 * @throws Error if analysis fails
 */
export async function analyzePassword(
  params: PasswordAnalyzeRequest,
): Promise<PasswordAnalyzeResponse> {
  try {
    const response = await analyzePasswordApiV1PasswordAnalyzePost({
      body: params,
    });

    if (response.error) {
      handleApiError(response.error);
    }

    if (!response.data) {
      throw new Error("No data received from server");
    }

    return response.data;
  } catch (err) {
    throw err;
  }
}

/**
 * Handle API errors and throw user-friendly messages
 */
function handleApiError(error: any): never {
  const detail = error.detail;

  if (Array.isArray(detail)) {
    const errors = detail.map((err: any) => err.msg).join(", ");
    throw new Error(`Validation error: ${errors}`);
  }

  if (typeof detail === "object" && detail !== null && "message" in detail) {
    throw new Error(detail.message || detail.code || "Request failed");
  }

  if (typeof detail === "string") {
    throw new Error(detail);
  }

  throw new Error("An unexpected error occurred");
}
