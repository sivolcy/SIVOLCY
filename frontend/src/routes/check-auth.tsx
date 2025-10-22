import React from "react";
import { Outlet, useSearchParams, useLocation } from "react-router";

/**
 * check-auth 布局（父级）
 * - 作用：在渲染 root-layout 之前检查 token 是否存在并可用
 * - 行为：
 *    - 没有 token -> 显示提示（不渲染 Outlet，root-layout 不会被挂载）
 *    - 有 token -> 可先异步验证（/api/options/config），验证通过后渲染 Outlet
 * 注意：所有 hook 必须在组件顶层调用，不能在分支中调用。
 *
 *
// export default [
//   layout("routes/check-auth.tsx", [
//     layout("routes/root-layout.tsx", [
//       index("routes/home.tsx"),
//       route("accept-tos", "routes/accept-tos.tsx"),
//       route("settings", "routes/settings.tsx", [
//         index("routes/llm-settings.tsx"),
//         route("mcp", "routes/mcp-settings.tsx"),
//         route("user", "routes/user-settings.tsx"),
//         route("integrations", "routes/git-settings.tsx"),
//         route("app", "routes/app-settings.tsx"),
//         route("billing", "routes/billing.tsx"),
//         route("secrets", "routes/secrets-settings.tsx"),
//         route("api-keys", "routes/api-keys.tsx"),
//       ]),
//       route("conversations/:conversationId", "routes/conversation.tsx"),
//       route("microagent-management", "routes/microagent-management.tsx"),
//     ]),
//   ]),
// ] satisfies RouteConfig;

 */
export default function CheckAuthLayout() {
  const [searchParams] = useSearchParams();
  const location = useLocation(); // <-- 获取当前路由信息

  // 从 URL 或 localStorage 获取 token
  const urlToken = searchParams.get("token");
  const localToken =
    typeof window !== "undefined" ? localStorage.getItem("jwt_token") : null;

  // 根据当前路径决定使用的 token
  const currentToken = React.useMemo(() => {
    if (location.pathname === "/") {
      // 如果是根路径 "/", 只考虑 URL 中的 token
      // ！！临时允许，在调试时使用！！
      // eslint-disable-next-line no-console
      console.log("#### On root path '/', checking only URL token.");
      return urlToken;
    }
    // 其他路径，URL token 优先，否则使用 localStorage 中的 token
    // eslint-disable-next-line no-console
    console.log(
      "#### On non-root path, checking URL token or localStorage token.",
    );
    return urlToken || localToken;
  }, [location.pathname, urlToken, localToken]); // 依赖项：路径和两个 token 来源

  // 如果 URL 中带 token，立即更新 localStorage（同步）
  // 这个逻辑在任何路径下都适用，目的是为了持久化通过 URL 传入的 token
  React.useEffect(() => {
    // Only update localStorage if urlToken exists and is different from the current localToken.
    // This prevents unnecessary writes and ensures the most recent valid token is stored.
    if (urlToken && urlToken !== localToken) {
      localStorage.setItem("jwt_token", urlToken);
      // eslint-disable-next-line no-console
      console.log("#### Saved URL token to localStorage.");
    }
  }, [urlToken, localToken]); // Depend on both to react to changes in either.

  // 本地状态：checking / unauthenticated / authenticated
  // Initialize status based on whether a token is available from URL or localStorage.
  const [status, setStatus] = React.useState<
    "checking" | "unauthenticated" | "authenticated"
  >(() => (currentToken ? "checking" : "unauthenticated"));

  // Effect to handle the actual token validation.
  // This effect will run whenever the 'token' derived state changes.

  // 异步验证 token（可选）
  React.useEffect(() => {
    let cancelled = false; // 声明在顶部，以便清理函数可以访问

    if (!currentToken) {
      setStatus("unauthenticated");
      // eslint-disable-next-line no-console
      console.log("#### No currentToken found, status set to unauthenticated.");
      // return;
      // 在这种情况下，不会启动异步操作，但 useEffect 仍会返回一个清理函数。
      // 清理函数在这里主要用于确保 'cancelled' 标志被设置，尽管在这种分支下它可能不会被使用。
    } else {
      // If a token is available, set status to checking and attempt validation.
      setStatus("checking"); // 开始验证，显示 "Authenticating..."
      // let cancelled = false;

      // 将异步验证逻辑封装在立即执行的 async 函数中
      (async () => {
        // eslint-disable-next-line no-console
        console.log(`#### Attempting to validate token: ${currentToken}`);

        try {
          // 发起简单请求验证 token
          const res = await fetch("/api/check_auth", {
            headers: {
              Authorization: `Bearer ${currentToken}`,
            },
          });

          if (cancelled) return;

          if (res.ok) {
            // eslint-disable-next-line no-console
            console.log("#### Token validation OK! ");
            // 验证通过，确保 token 存在于 localStorage 中（即使它最初来自 URL 且路径是 /）
            localStorage.setItem("jwt_token", currentToken);
            setStatus("authenticated");
          } else {
            // eslint-disable-next-line no-console
            console.log("#### Token validation BAD! ");
            // token 无效，从 localStorage 中移除
            localStorage.removeItem("jwt_token");
            setStatus("unauthenticated");
          }
        } catch (err) {
          // eslint-disable-next-line no-console
          console.log(`#### response ERR! ${err}`);
          if (!cancelled) {
            // 出错时视为未认证（可调整为重试或显示错误）
            // Network error or other fetch issues, consider unauthenticated and clear potentially stale token.
            localStorage.removeItem("jwt_token");
            setStatus("unauthenticated");
          }
        }
      })(); // <-- 立即执行
    }

    // useEffect 的回调函数始终返回这个清理函数
    return () => {
      cancelled = true; // 清理函数
    };
  }, [currentToken]); // Re-run this effect whenever the 'token' (urlToken || localToken) changes.

  // 根据状态渲染：注意：只有 status === 'authenticated' 时才渲染 Outlet（即 root-layout）
  if (status === "unauthenticated") {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-3xl font-semibold">
          Please authenticate to continue...
        </div>
      </div>
    );
  }

  if (status === "checking") {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-3xl font-semibold">Authenticating...</div>
      </div>
    );
  }

  // 认证通过，渲染下层路由（root-layout 及其子路由）
  return <Outlet />;
}
