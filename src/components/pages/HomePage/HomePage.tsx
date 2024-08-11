/**
 * Landing Page
 * @returns
 */
import { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useLocation } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL;
// const API_URL = import.meta.env.VITE_DEV_API_URL;

const HomePage = () => {
  const [status, setStatus] = useState("");
  const location = useLocation().pathname;
  const params = useParams();

  console.log(API_URL + location);
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}` + location, {
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (response.headers["content-type"].includes("application/json")) {
          setStatus(response.data);
        } else {
          console.error("Received non-JSON response:", response.data);
          setStatus("Unexpected response format");
        }
      } catch (error) {
        console.error("Error fetching status:", error);
        setStatus("Game 7 OT loss to Server");
      }
    };
    fetchStatus();
  }, []);
  return <div>{status}</div>;
};

export default HomePage;
