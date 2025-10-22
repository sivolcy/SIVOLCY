import axios, { AxiosError, AxiosResponse } from "axios";

export const openHands = axios.create({
  baseURL: `${window.location.protocol}//${import.meta.env.VITE_BACKEND_BASE_URL || window?.location.host}`,
});

// Helper function to check if a response contains an email verification error
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const checkForEmailVerificationError = (data: any): boolean => {
  const EMAIL_NOT_VERIFIED = "EmailNotVerifiedError";

  if (typeof data === "string") {
    return data.includes(EMAIL_NOT_VERIFIED);
  }

  if (typeof data === "object" && data !== null) {
    if ("message" in data) {
      const { message } = data;
      if (typeof message === "string") {
        return message.includes(EMAIL_NOT_VERIFIED);
      }
      if (Array.isArray(message)) {
        return message.some(
          (msg) => typeof msg === "string" && msg.includes(EMAIL_NOT_VERIFIED),
        );
      }
    }

    // Search any values in object in case message key is different
    return Object.values(data).some(
      (value) =>
        (typeof value === "string" && value.includes(EMAIL_NOT_VERIFIED)) ||
        (Array.isArray(value) &&
          value.some(
            (v) => typeof v === "string" && v.includes(EMAIL_NOT_VERIFIED),
          )),
    );
  }

  return false;
};

// 请求拦截器: 自动添加 Authorization header
openHands.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwt_token");

    // ！！临时允许，在调试时使用！！
    // eslint-disable-next-line no-console
    console.log(
      `#### openHands.interceptors: url: ${config.url}, set token: ${token}`,
    );

    // Git pre-commit hook hit error : no-param-reassign
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }

    if (token) {
      // 使用 AxiosHeaders 的 set 方法，类型安全且不触发 no-param-reassign
      config.headers.set("Authorization", `Bearer ${token}`);
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// Set up the global interceptor
openHands.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    // Check if it's a 403 error with the email verification message
    if (
      error.response?.status === 403 &&
      checkForEmailVerificationError(error.response?.data)
    ) {
      if (window.location.pathname !== "/settings/user") {
        window.location.reload();
      }
    }

    // // 处理 401 错误: 清除 token 并重定向到认证页面
    // if (error.response?.status === 401) {
    //   localStorage.removeItem('jwt_token');
    //   // 如果不在认证页面,重定向到认证页面
    //   if (window.location.pathname !== '/auth') {
    //     window.location.href = '/auth';
    //   }
    // }

    // Continue with the error for other error handlers
    return Promise.reject(error);
  },
);
