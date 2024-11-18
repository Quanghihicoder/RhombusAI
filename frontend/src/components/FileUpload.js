import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await axios.post(
        "http://localhost:8000/myapp/upload-csv/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResponse(res.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const renderTable = (data) => (
    <table>
      <thead>
        <tr>
          <th>Column Name</th>
          <th>Data Type</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(data).map(([key, value]) => {
          switch (value) {
            case "object":
              value = "Text";
              break;
            case "int64":
              value = "Integer 64 bits";
              break;
            case "int32":
              value = "Integer 32 bits";
              break;
            case "int16":
              value = "Integer 16 bits";
              break;
            case "int8":
              value = "Integer 8 bits";
              break;
            case "float64":
              value = "Float 64 bits";
              break;
            case "float32":
              value = "Float 32 bits";
              break;
            case "bool":
              value = "Boolean";
              break;
            case "datetime64[ns]":
              value = "Date";
              break;
            case "timedelta64[ns]":
              value = "Time";
              break;
            case "category":
              value = "Category";
              break;
            case "complex128":
              value = "Complex";
              break;
            default:
              break;
          }

          return (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );

  return (
    <div className="container">
      <div className="uploadContainer">
        <h2>Upload a CSV file</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
      </div>

      {response && (
        <div className="responseContainer">
          <div className="responseTable">
            <h3>Before Conversion:</h3>
            {renderTable(response.dtypes_before)}
          </div>
          <div className="responseTable">
            <h3>After Conversion:</h3>
            {renderTable(response.dtypes_after)}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
