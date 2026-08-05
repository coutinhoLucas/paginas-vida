-- Execute uma vez no SQL Editor do projeto Supabase.
create table if not exists public.controle (
  id integer primary key,
  modo text not null check (modo in ('experiencia', 'revelacao', 'conclusao')),
  modo_anterior text check (modo_anterior in ('experiencia', 'revelacao', 'conclusao')),
  atualizado_em timestamptz not null default now()
);
insert into public.controle (id, modo) values (1, 'experiencia') on conflict (id) do nothing;
alter table public.controle enable row level security;
create policy "Leitura pública do modo" on public.controle for select to anon, authenticated using (id = 1);
create policy "Alteração somente autenticada" on public.controle for update to authenticated using (id = 1) with check (id = 1);
