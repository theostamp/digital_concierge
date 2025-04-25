// frontend/app/supervisor/[tenantId]/page.tsx

"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { UICard, UICardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import axios from "axios";

interface Tenant {
  id: number;
  name: string;
  schema_name: string;
  domain_url: string;
}

export default function TenantDetailPage() {
  const router = useRouter();
  const params = useRouter().params || ({} as { tenantId?: string });
  const tenantId = params?.tenantId;

  const [tenant, setTenant] = useState<Tenant | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (tenantId) {
      fetchTenant();
    }
  }, [tenantId]);

  const fetchTenant = async () => {
    try {
      const res = await axios.get(`/api/tenants/${tenantId}/`);
      setTenant(res.data);
    } catch (error) {
      console.error("Error fetching tenant:", error);
    } finally {
      setLoading(false);
    }
  };

  let content;
  if (loading) {
    content = <p>Loading...</p>;
  } else if (tenant) {
    content = (
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
    );
  } else {
    content = <p className="text-red-500">Tenant not found.</p>;
  }

  return (
    <div className="p-6">
      <Button variant="outline" onClick={() => router.back()} className="mb-4">
        ← Back
      </Button>
      {content}
    </div>
  );
}
