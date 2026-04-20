'use client';

import { useRedirectFirstChild } from '@/hooks/useRedirectFirstChild';
import { useUserApi } from '@/app/system-manager/api/user/index';

export default function UserPage() {
  useRedirectFirstChild();
  return null;
}
