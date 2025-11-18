import './config';

import { generateQrCodeApiV1QrGeneratePost, scanQrCodeApiV1QrScanPost } from './generated/sdk.gen';
import type {
  QrCodeRequest,
  QrCodeResponse,
  ErrorCorrection,
  ModuleDrawerType,
  EyeDrawerType,
  ColorMaskType,
  ModuleDrawerConfig,
  EyeDrawerConfig,
  ColorMaskConfig,
  QrScanRequest,
  QrScanResponse
} from './generated/types.gen';

export type QRCodeRequest = QrCodeRequest;
export type QRCodeResponse = QrCodeResponse;
export type ErrorCorrectionLevel = ErrorCorrection;

export type QRScanRequest = QrScanRequest;
export type QRScanResponse = QrScanResponse;

export type { 
  ModuleDrawerType, 
  EyeDrawerType, 
  ColorMaskType,
  ModuleDrawerConfig,
  EyeDrawerConfig,
  ColorMaskConfig,
};

/**
 * Generate QR code with comprehensive styling options
 * 
 * @param params - QR code generation parameters
 * @returns Promise<QRCodeResponse> - Generated QR code data
 * @throws Error if generation fails
 */
export async function generateQRCode(params: QRCodeRequest): Promise<QRCodeResponse> {
  try {
    const response = await generateQrCodeApiV1QrGeneratePost({
      body: params,
    });

    if (response.error) {
      handleApiError(response.error);
    }

    if (!response.data) {
      throw new Error('No data received from server');
    }

    return response.data;
  } catch (err) {
    throw err;
  }
}

/**
 * Scan and decode QR code(s) from an image
 * 
 * @param params - Scan request parameters (image base64, auto_resize)
 * @returns Promise<QRScanResponse> - Decoded QR codes
 * @throws Error if scan fails or no QR codes found
 * 
 * @example
 * ```
 * const result = await scanQRCode({
 *   image: "data:image/png;base64,iVBORw0KGg...",
 *   auto_resize: true
 * });
 * 
 * console.log(`Found ${result.count} QR code(s):`);
 * result.codes.forEach(code => console.log(code));
 * ```
 */
export async function scanQRCode(params: QRScanRequest): Promise<QRScanResponse> {
  try {
    const response = await scanQrCodeApiV1QrScanPost({
      body: params,
    });

    if (response.error) {
      handleApiError(response.error);
    }

    if (!response.data) {
      throw new Error('No data received from server');
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
    const errors = detail.map((err: any) => err.msg).join(', ');
    throw new Error(`Validation error: ${errors}`);
  }

  if (typeof detail === 'object' && detail !== null && 'message' in detail) {
    throw new Error(detail.message || detail.code || 'Request failed');
  }

  if (typeof detail === 'string') {
    throw new Error(detail);
  }

  throw new Error('An unexpected error occurred');
}
