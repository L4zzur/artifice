import "./config";
import {
  generateHashApiV1HashGeneratePost,
  hashFileApiV1HashFilePost,
  listAlgorithmsApiV1HashAlgorithmsGet,
  verifyHashApiV1HashVerifyPost,
  type HashAlgorithmSchema,
  type HashFileRequest,
  type HashFileResponse,
  type HashGenerateRequest,
  type HashGenerateResponse,
  type HashVerifyRequest,
  type HashVerifyResponse,
} from "./generated";

/**
 * Generate hash from data
 *
 * @param params - Hash generation parameters
 * @returns Generated hash data
 * @throws Error if generation fails
 * */
export async function generateHash(
  params: HashGenerateRequest,
): Promise<HashGenerateResponse> {
  const response = await generateHashApiV1HashGeneratePost({
    body: params,
  });

  if (response.error) {
    handleApiError(response.error);
  }

  if (!response.data) {
    throw new Error("No data received from server");
  }

  return response.data;
}

/**
 * Verify hash
 *
 * @param params - Hash verification parameters
 * @returns Verified hash data
 * @throws Error if verification fails
 * */
export async function verifyHash(
  params: HashVerifyRequest,
): Promise<HashVerifyResponse> {
  const response = await verifyHashApiV1HashVerifyPost({
    body: params,
  });

  if (response.error) {
    handleApiError(response.error);
  }

  if (!response.data) {
    throw new Error("No data received from server");
  }

  return response.data;
}

/**
 * Hash file
 *
 * @param params - File hashing parameters
 * @returns Hashed file data
 * @throws Error if hashing fails
 * */
export async function hashFile(
  params: HashFileRequest,
): Promise<HashFileResponse> {
  const response = await hashFileApiV1HashFilePost({
    body: params,
  });

  if (response.error) {
    handleApiError(response.error);
  }

  if (!response.data) {
    throw new Error("No data received from server");
  }

  return response.data;
}

/**
 * List available hash algorithms
 *
 * @returns List of available hash algorithms
 * @throws Error if listing fails
 * */
export async function listHashAlgorithms(): Promise<HashAlgorithmSchema[]> {
  const response = await listAlgorithmsApiV1HashAlgorithmsGet();

  if (response.error) {
    handleApiError(response.error);
  }

  if (!response.data) {
    throw new Error("No data received from server");
  }

  return response.data;
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
