import { API_BASE_URL } from "../config";
import { useState } from "react";

export default function NetURL() {
  const [baseURL, setBaseURL] = useState(
    localStorage.getItem("NetURL") || API_BASE_URL
  );

  return (
    <div className="NetURL">
      <div>
        <input
          type="text"
          placeholder="NetURL"
          value={baseURL}
          onChange={(e) => setBaseURL(e.target.value)}
        />
        <button
          onClick={() => {
            // Add to localStorage
            localStorage.setItem("NetURL", baseURL);
            // Reload page
            window.location.reload();
          }}
        >
          Fetch
        </button>
      </div>
      <br />
    </div>
  );
}
