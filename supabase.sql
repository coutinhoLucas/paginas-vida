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
create policy "Alteração somente pelo administrador"
on public.controle for update to authenticated
using (id = 1 and (auth.jwt()->>'email') = 'lucascousan@gmail.com')
with check (id = 1 and (auth.jwt()->>'email') = 'lucascousan@gmail.com');

-- Canal público sem cabeçalhos especiais para leitura confiável nos celulares.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('controle', 'controle', true, 10240, array['application/json'])
on conflict (id) do update set public = true;

create policy "Administrador insere estado"
on storage.objects for insert to authenticated
with check (bucket_id = 'controle' and (auth.jwt()->>'email') = 'lucascousan@gmail.com');

-- A atualização de um arquivo existente também exige permissão de leitura da linha.
create policy "Administrador lê estado"
on storage.objects for select to authenticated
using (bucket_id = 'controle' and (auth.jwt()->>'email') = 'lucascousan@gmail.com');

create policy "Administrador atualiza estado"
on storage.objects for update to authenticated
using (bucket_id = 'controle' and (auth.jwt()->>'email') = 'lucascousan@gmail.com')
with check (bucket_id = 'controle' and (auth.jwt()->>'email') = 'lucascousan@gmail.com');
