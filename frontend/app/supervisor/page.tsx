// frontend/app/supervisor/page.tsx

"use client";

import { UICard, UICardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import axios from "axios";

interface Tenant {
  id: number;
  name: string;
  schema_name: string;
  domain_url: string;
}

export default function SupervisorDashboard() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [newTenantName, setNewTenantName] = useState("");
  const [newTenantSchema, setNewTenantSchema] = useState("");

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      const res = await axios.get("/api/tenants/");
      setTenants(res.data);
    } catch (error) {
      console.error("Error fetching tenants:", error);
    }
  };

  const handleCreateTenant = async () => {
    try {
      await axios.post("/api/tenants/", {
        name: newTenantName,
        schema_name: newTenantSchema,
      });
      setNewTenantName("");
      setNewTenantSchema("");
      fetchTenants();
    } catch (error) {
      console.error("Error creating tenant:", error);
    }
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-2xl font-bold">Supervisor Dashboard</h1>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Tenant Name"
          value={newTenantName}
          onChange={(e) => setNewTenantName(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="text"
          placeholder="Schema Name"
          value={newTenantSchema}
          onChange={(e) => setNewTenantSchema(e.target.value)}
          className="border p-2 rounded"
        />
        <Button onClick={handleCreateTenant}>+ Create Tenant</Button>
      </div>

      {tenants.length === 0 ? (
        <p className="text-gray-500 mt-4">No tenants found.</p>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {tenants.map((tenant) => (
            <div key={tenant.id}>
              <UICard className="hover:shadow-md transition">
                <UICardContent className="p-4">
                  <div>
                    <h2 className="text-xl font-semibold">{tenant.name}</h2>
                    <p className="text-sm text-gray-500">Schema: {tenant.schema_name}</p>
                    <p className="text-sm text-gray-500">Domain: {tenant.domain_url}</p>
                    <Button variant="outline" className="mt-4">
                      Manage
                    </Button>
                  </div>
                </UICardContent>
              </UICard>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}