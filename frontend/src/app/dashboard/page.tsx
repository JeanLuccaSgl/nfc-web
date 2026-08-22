"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { supabase } from "@/lib/supabase";

import styles from "./page.module.css";

type DashboardData = {
  empresa: {
    id: number;
    nome: string;
  };
  estatisticas: {
    acessos_hoje: number;
    acessos_ultimos_7_dias: number;
    total_acessos: number;
    acessos_qr: number;
    acessos_nfc: number;
    ultimo_acesso: string | null;
  };
  qr_atual: {
    codigo: string;
    destino_url: string;
    ativo: boolean;
  } | null;
  acessos_recentes: Array<{
    codigo: string;
    origem: "qr" | "nfc";
    acessado_em: string;
  }>;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

function formatarData(data: string | null) {
  if (!data) return "Nenhum acesso registrado";

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(data));
}

export default function DashboardPage() {
  const router = useRouter();
  const [dados, setDados] = useState<DashboardData | null>(null);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregarDashboard() {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) {
        router.replace("/");
        return;
      }

      if (!apiUrl) {
        setErro("A URL da API não foi configurada.");
        setCarregando(false);
        return;
      }

      const resposta = await fetch(`${apiUrl}/dashboard/overview`, {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      if (resposta.status === 401) {
        await supabase.auth.signOut();
        router.replace("/");
        return;
      }

      if (!resposta.ok) {
        setErro("Não foi possível carregar os dados do dashboard.");
        setCarregando(false);
        return;
      }

      setDados(await resposta.json());
      setCarregando(false);
    }

    carregarDashboard().catch(() => {
      setErro("Não foi possível conectar ao backend.");
      setCarregando(false);
    });
  }, [router]);

  async function sair() {
    await supabase.auth.signOut();
    router.replace("/");
  }

  if (carregando) {
    return <main className={styles.state}>Carregando seu painel...</main>;
  }

  if (erro || !dados) {
    return (
      <main className={styles.state}>
        <p>{erro || "Nenhum dado disponível."}</p>
        <button onClick={() => window.location.reload()}>Tentar novamente</button>
      </main>
    );
  }

  const { estatisticas, qr_atual: qrAtual } = dados;

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <span className={styles.brandMark}>NL</span>
          <span>NFC</span>
        </div>

        <div className={styles.headerActions}>
          <span className={styles.clientName}>{dados.empresa.nome}</span>
          <button className={styles.logoutButton} onClick={sair}>
            Sair
          </button>
        </div>
      </header>

      <section className={styles.content}>
        <div className={styles.heading}>
          <div>
            <p className={styles.eyebrow}>Visão geral</p>
            <h1>Olá, {dados.empresa.nome}.</h1>
            <p>Acompanhe como seus clientes estão chegando à avaliação.</p>
          </div>
          <span className={styles.liveStatus}>● Dados atualizados</span>
        </div>

        <section className={styles.metrics} aria-label="Resumo de acessos">
          <article className={styles.metricCard}>
            <span>Acessos hoje</span>
            <strong>{estatisticas.acessos_hoje}</strong>
            <small>Leituras registradas hoje</small>
          </article>
          <article className={styles.metricCard}>
            <span>Últimos 7 dias</span>
            <strong>{estatisticas.acessos_ultimos_7_dias}</strong>
            <small>Movimento recente</small>
          </article>
          <article className={styles.metricCard}>
            <span>QR Code</span>
            <strong>{estatisticas.acessos_qr}</strong>
            <small>Acessos identificados</small>
          </article>
          <article className={styles.metricCard}>
            <span>NFC</span>
            <strong>{estatisticas.acessos_nfc}</strong>
            <small>Acessos identificados</small>
          </article>
        </section>

        <section className={styles.mainGrid}>
          <article className={styles.panel}>
            <div className={styles.panelHeading}>
              <div>
                <p className={styles.eyebrow}>Atividade</p>
                <h2>Acessos recentes</h2>
              </div>
              <span className={styles.totalLabel}>
                {estatisticas.total_acessos} no total
              </span>
            </div>

            {dados.acessos_recentes.length === 0 ? (
              <p className={styles.emptyState}>
                Os acessos aparecerão aqui assim que alguém ler o QR Code ou a tag NFC.
              </p>
            ) : (
              <div className={styles.accessList}>
                {dados.acessos_recentes.map((acesso, index) => (
                  <div className={styles.accessRow} key={`${acesso.acessado_em}-${index}`}>
                    <span
                      className={`${styles.sourceIcon} ${
                        acesso.origem === "nfc" ? styles.nfcIcon : ""
                      }`}
                    >
                      {acesso.origem === "nfc" ? "NFC" : "QR"}
                    </span>
                    <div>
                      <strong>{acesso.origem === "nfc" ? "Tag NFC" : "QR Code"}</strong>
                      <span>Código {acesso.codigo}</span>
                    </div>
                    <time dateTime={acesso.acessado_em}>
                      {formatarData(acesso.acessado_em)}
                    </time>
                  </div>
                ))}
              </div>
            )}
          </article>

          <article className={styles.panel}>
            <div className={styles.panelHeading}>
              <div>
                <p className={styles.eyebrow}>Seu QR Code</p>
                <h2>Destino atual</h2>
              </div>
              <span className={qrAtual?.ativo ? styles.activeTag : styles.inactiveTag}>
                {qrAtual?.ativo ? "Ativo" : "Inativo"}
              </span>
            </div>

            {qrAtual ? (
              <div className={styles.destination}>
                <span className={styles.qrCode}>{qrAtual.codigo}</span>
                <p>{qrAtual.destino_url}</p>
                <small>O destino pode ser alterado sem gerar outro QR Code.</small>
              </div>
            ) : (
              <p className={styles.emptyState}>Nenhum QR Code cadastrado.</p>
            )}

            <div className={styles.lastAccess}>
              <span>Último acesso</span>
              <strong>{formatarData(estatisticas.ultimo_acesso)}</strong>
            </div>
          </article>
        </section>
      </section>
    </main>
  );
}
