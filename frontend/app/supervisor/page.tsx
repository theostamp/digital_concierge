"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import axios from "axios";

export default function SupervisorDashboard() {
  const [tenants, setTenants] = useState([]);

  useEffect(() => {
    axios.get("/api/tenants/").then((res) => setTenants(res.data));
  }, []);

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-2xl font-bold">Supervisor Dashboard</h1>

      {tenants.length === 0 ? (
        <p className="text-gray-500">No tenants found.</p>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tenants.map((tenant) => (
            <div key={tenant.id}>
              <Card className="hover:shadow-md transition">
                <CardContent className="p-4">
                  <h2 className="text-xl font-semibold">{tenant.name}</h2>
                  <p className="text-sm text-gray-500">Schema: {tenant.schema_name}</p>
                  <Button variant="outline" className="mt-4">
                    Manage
                  </Button>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
