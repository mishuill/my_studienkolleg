import { useState } from "react";

const CustomInput = ({
    type = "text",
    description="",
    name,
    label,
    error,
    ExternalState,
    setExternalState,
    inputStyles,
    required,
    ...props

  }) => {
    const [validity, setValidity] = useState(!required)
    const handleChange = (e) => {
      const { name, value } = e.target;
      setExternalState({ ...ExternalState, [name]: value });
      setValidity(e.target.checkValidity())
    };
  
    return (
      <div style={inputStyles.container}>
        {label ? <label htmlFor={name}>{label}</label> : null}
        <input
          type={type}
          id={name}
          name={name}
          value={ExternalState.name}
          onChange={handleChange}
          style={validity ? inputStyles.valid : inputStyles.invalid}
          required={required}
          {...props}
        />
        {description ? <span style={inputStyles.description}>{description}</span> : null}
        {error ? <span style={inputStyles.error}>{error}</span> : null}
      </div>
    );
  };

  const CustomTextArea = ({
    type = "text",
    description="",
    name,
    label,
    error,
    ExternalState,
    setExternalState,
    inputStyles,
    required,
    ...props

  }) => {
    const [validity, setValidity] = useState(!required)
    const handleChange = (e) => {
      const { name, value } = e.target;
      setExternalState({ ...ExternalState, [name]: value });
      setValidity(e.target.checkValidity())
    };
  
    return (
      <div style={inputStyles.container}>
        {label ? <label htmlFor={name}>{label}</label> : null}
        <textarea
          type={type}
          id={name}
          name={name}
          value={ExternalState.name}
          onChange={handleChange}
          style={validity ? inputStyles.valid : inputStyles.invalid}
          required={required}
          {...props}
        />
        {description ? <span style={inputStyles.description}>{description}</span> : null}
        {error ? <span style={inputStyles.error}>{error}</span> : null}
      </div>
    );
  };
  
  const DefaultTextArea = (props) => {
    const InputStyles = {
      container: { marginBottom: "20px" },
      valid: {
        display: "block",
        padding: "8px",
        border: "1px solid #ccc",
        borderRadius: "4px",
        marginTop: "5px",
      },
      invalid: {
        display: "block",
        padding: "8px",
        border: "1px solid #fc6d00",
        backgrond: "#ffedd9",
        borderRadius: "4px",
        marginTop: "5px",
      },
      description: {},
      error: { color: "red"}
    }
    return <CustomTextArea inputStyles={InputStyles} {...props}/>
  }

  const DefaultInput = (props) => {
    const InputStyles = {
      container: { marginBottom: "20px" },
      valid: {
        display: "block",
        padding: "8px",
        border: "1px solid #ccc",
        borderRadius: "4px",
        marginTop: "5px",
      },
      invalid: {
        display: "block",
        padding: "8px",
        border: "1px solid #fc6d00",
        backgrond: "#ffedd9",
        borderRadius: "4px",
        marginTop: "5px",
      },
      description: {},
      error: { color: "red"}
    }
    return <CustomInput inputStyles={InputStyles} {...props}/>
  };

export {DefaultInput, DefaultTextArea, CustomInput, CustomTextArea}