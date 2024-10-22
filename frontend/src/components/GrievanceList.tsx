import React, { useEffect, useState } from "react";
import axios from "axios";

// Define the type for the grievance record
interface Grievance {
  id: number;
  source: string;
  edit_source?: string | null; // optional or can be null
  sentiment_anaylis?: string | null; // optional or can be null
}

const GrievanceList: React.FC = () => {
  const [grievances, setGrievances] = useState<Grievance[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGrievances = async () => {
      try {
        const response = await axios.get<Grievance[]>(
          "http://localhost:5000/get_grievance_records"
        );
        setGrievances(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchGrievances();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Grievance Records</h2>
      <ul>
        {grievances.map((grievance) => (
          <li key={grievance.id}>
            <p>
              <strong>ID:</strong> {grievance.id}
            </p>
            <p>
              <strong>Source:</strong> {grievance.source}
            </p>
            <p>
              <strong>Edit Source:</strong> {grievance.edit_source || "None"}
            </p>
            <p>
              <strong>Sentiment Analysis:</strong>{" "}
              {grievance.sentiment_anaylis || "None"}
            </p>
            <hr />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GrievanceList;
