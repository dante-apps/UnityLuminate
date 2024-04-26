export function getValidationRules(rules) {
  const validationRules = [];

  for (const rule of rules) {
    const [ruleName, ruleParam] = rule.split(":");

    switch (ruleName) {
      case "required":
        validationRules.push((v) => !!v || "Field is required");
        break;
      case "email":
        validationRules.push(
          (v) =>
            /^[^\s@]+@[^\s@]+\.(com|cloud|net|org.in|org|edu|gov|auroville|in...)$/.test(
              v
            ) || "Email must be valid"
        );
        break;
      case "min":
        validationRules.push(
          (v) =>
            (v && typeof v === "number" && v >= parseInt(ruleParam, 10)) ||
            `Minimum value is ${ruleParam}`
        );
        break;
      case "max":
        validationRules.push(
          (v) =>
            (v && typeof v === "number" && v <= parseInt(ruleParam, 10)) ||
            `Maximum value is ${ruleParam}`
        );
        break;
    }
  }

  return validationRules;
}
