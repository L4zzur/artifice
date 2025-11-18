import './config';

import { generateQrCodeApiV1QrGeneratePost } from './generated/sdk.gen';
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
} from './generated/types.gen';

export type QRCodeRequest = QrCodeRequest;
export type QRCodeResponse = QrCodeResponse;
export type ErrorCorrectionLevel = ErrorCorrection;
export type { 
  ModuleDrawerType, 
  EyeDrawerType, 
  ColorMaskType,
  ModuleDrawerConfig,
  EyeDrawerConfig,
  ColorMaskConfig,
};

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
