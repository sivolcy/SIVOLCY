import { Autocomplete, AutocompleteItem } from "@heroui/react";
import React from "react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";

import { cn } from "#/utils/utils";

// 【修改1】简化接口: 移除 models 参数,因为模型列表现在是固定的
interface ModelSelectorProps {
  isDisabled?: boolean;
  // models: Record<string, { separator: string; models: string[] }>;
  currentModel?: string;
  onChange?: (model: string | null) => void;
  wrapperClassName?: string;
  labelClassName?: string;
}

// 【修改2】新增: 定义固定的模型列表
const AVAILABLE_MODELS = [
  "gpt-5",
  "gpt-5-mini",
  "gpt-4.1",
  "claude-opus-4",
  "claude-3-5-haiku",
];
const DEFAULT_MODEL = "gpt-5-mini";

export function ModelSelector({
  isDisabled,
  // models,
  currentModel,
  onChange,
  wrapperClassName,
  labelClassName,
}: ModelSelectorProps) {
  // 【修改3】简化状态: 只需要跟踪选中的模型,不需要 provider 和 litellmId
  // const [, setLitellmId] = React.useState<string | null>(null);
  // const [selectedProvider, setSelectedProvider] = React.useState<string | null>(
  //   null,
  // );
  const [selectedModel, setSelectedModel] = React.useState<string | null>(null);
  const { t } = useTranslation();

  // // Get the appropriate verified models array based on the selected provider
  // const getVerifiedModels = () => {
  //   if (selectedProvider === "openhands") {
  //     return VERIFIED_OPENHANDS_MODELS;
  //   }
  //   return VERIFIED_MODELS;
  // };

  // 【修改4】简化初始化: 直接使用 currentModel,不需要解析 provider
  React.useEffect(() => {
    if (currentModel) {
      setSelectedModel(currentModel);
      // runs when resetting to defaults
      // const { provider, model } = extractModelAndProvider(currentModel);
      // setLitellmId(currentModel);
      // setSelectedProvider(provider);
      // setSelectedModel(model);
    } else {
      setSelectedModel(DEFAULT_MODEL);
    }
  }, [currentModel]);

  // 【修改5】简化处理: 直接设置模型,不需要拼接 provider
  const handleChangeModel = (model: string) => {
    setSelectedModel(model);
    onChange?.(model);
  };
  // const handleChangeProvider = (provider: string) => {
  //   setSelectedProvider(provider);
  //   setSelectedModel(null);
  //
  //   const separator = models[provider]?.separator || "";
  //   setLitellmId(provider + separator);
  // };

  // const handleChangeModel = (model: string) => {
  //   const separator = models[selectedProvider || ""]?.separator || "";
  //   let fullModel = selectedProvider + separator + model;
  //   if (selectedProvider === "openai") {
  //     // LiteLLM lists OpenAI models without the openai/ prefix
  //     fullModel = model;
  //   }
  //   setLitellmId(fullModel);
  //   setSelectedModel(model);
  //   onChange?.(fullModel);
  // };

  // 【修改6】移除: clear 函数和 handleChangeProvider 函数
  // 因为不再需要 provider 选择
  // const clear = () => {
  //   setSelectedProvider(null);
  //   setLitellmId(null);
  // };

  // const { t } = useTranslation();

  return (
    // 【修改7】简化布局: 移除双列布局,只保留单个模型选择器
    <div
      className={cn(
        "flex flex-col md:flex-row w-[full] max-w-[680px] justify-between gap-4 md:gap-[46px]",
        wrapperClassName,
      )}
    >
      <fieldset className="flex flex-col gap-2.5 w-full">
        <label className={cn("text-sm", labelClassName)}>
          {t(I18nKey.LLM$PROVIDER)}
        </label>
        <Autocomplete
          data-testid="llm-provider-input"
          isRequired
          isVirtualized={false}
          name="llm-provider-input"
          // isDisabled={isDisabled}
          aria-label={t(I18nKey.LLM$PROVIDER)}
          placeholder={t(I18nKey.LLM$SELECT_PROVIDER_PLACEHOLDER)}
          isClearable={false}
          onSelectionChange={(e) => {
            if (e?.toString()) handleChangeModel(e.toString());
          }}
          isDisabled={isDisabled}
          selectedKey={selectedModel}
          defaultSelectedKey={selectedModel ?? DEFAULT_MODEL}
          // onSelectionChange={(e) => {
          //   if (e?.toString()) handleChangeProvider(e.toString());
          // }}
          // onInputChange={(value) => !value && clear()}
          // defaultSelectedKey={selectedProvider ?? undefined}
          // selectedKey={selectedProvider}
          classNames={{
            popoverContent: "bg-tertiary rounded-xl border border-[#717888]",
          }}
          inputProps={{
            classNames: {
              inputWrapper:
                "bg-tertiary border border-[#717888] h-10 w-full rounded-sm p-2 placeholder:italic",
            },
          }}
        >
          {/* 【修改8】简化选项: 直接渲染固定的模型列表,移除分组逻辑 */}
          {AVAILABLE_MODELS.map((model) => (
            <AutocompleteItem key={model} data-testid={`model-item-${model}`}>
              {model}
            </AutocompleteItem>
          ))}
        </Autocomplete>
        {/* <AutocompleteSection title={t(I18nKey.MODEL_SELECTOR$VERIFIED)}>
            {VERIFIED_PROVIDERS.filter((provider) => models[provider]).map(
              (provider) => (
                <AutocompleteItem
                  data-testid={`provider-item-${provider}`}
                  key={provider}
                >
                  {mapProvider(provider)}
                </AutocompleteItem>
              ),
            )}
          </AutocompleteSection> */}
        {/* {Object.keys(models).some(
            (provider) => !VERIFIED_PROVIDERS.includes(provider),
          ) ? (
            <AutocompleteSection title={t(I18nKey.MODEL_SELECTOR$OTHERS)}>
              {Object.keys(models)
                .filter((provider) => !VERIFIED_PROVIDERS.includes(provider))
                .map((provider) => (
                  <AutocompleteItem key={provider}>
                    {mapProvider(provider)}
                  </AutocompleteItem>
                ))}
            </AutocompleteSection>
          ) : null}
        </Autocomplete> */}
      </fieldset>

      {/* 【修改9】移除: Provider 选择器的整个 fieldset */}
      {/* 【修改10】移除: OpenHands 账户帮助链接 */}
      {/* {selectedProvider === "openhands" && (
        <HelpLink
          testId="openhands-account-help"
          text={t(I18nKey.SETTINGS$NEED_OPENHANDS_ACCOUNT)}
          linkText={t(I18nKey.SETTINGS$CLICK_HERE)}
          href={PRODUCT_URL.PRODUCTION}
          size="settings"
          linkColor="white"
        />
      )} */}
      {/* 【修改11】移除: 所有 AutocompleteSection 分组逻辑 */}
      {/* <fieldset className="flex flex-col gap-2.5 w-full">
        <label className={cn("text-sm", labelClassName)}>
          {t(I18nKey.LLM$MODEL)}
        </label>
        <Autocomplete
          data-testid="llm-model-input"
          isRequired
          isVirtualized={false}
          name="llm-model-input"
          aria-label={t(I18nKey.LLM$MODEL)}
          placeholder={t(I18nKey.LLM$SELECT_MODEL_PLACEHOLDER)}
          isClearable={false}
          onSelectionChange={(e) => {
            if (e?.toString()) handleChangeModel(e.toString());
          }}
          isDisabled={isDisabled || !selectedProvider}
          selectedKey={selectedModel}
          defaultSelectedKey={selectedModel ?? undefined}
          classNames={{
            popoverContent: "bg-tertiary rounded-xl border border-[#717888]",
          }}
          inputProps={{
            classNames: {
              inputWrapper:
                "bg-tertiary border border-[#717888] h-10 w-full rounded-sm p-2 placeholder:italic",
            },
          }}
        >
          <AutocompleteSection title={t(I18nKey.MODEL_SELECTOR$VERIFIED)}>
            {getVerifiedModels()
              .filter((model) =>
                models[selectedProvider || ""]?.models?.includes(model),
              )
              .map((model) => (
                <AutocompleteItem key={model}>{model}</AutocompleteItem>
              ))}
          </AutocompleteSection>
          {models[selectedProvider || ""]?.models?.some(
            (model) => !getVerifiedModels().includes(model),
          ) ? (
            <AutocompleteSection title={t(I18nKey.MODEL_SELECTOR$OTHERS)}>
              {models[selectedProvider || ""]?.models
                .filter((model) => !getVerifiedModels().includes(model))
                .map((model) => (
                  <AutocompleteItem
                    data-testid={`model-item-${model}`}
                    key={model}
                  >
                    {model}
                  </AutocompleteItem>
                ))}
            </AutocompleteSection>
          ) : null}
        </Autocomplete>
      </fieldset> */}
    </div>
  );
}
