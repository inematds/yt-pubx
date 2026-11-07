| data | o que quebrou | menor correção | tipo |
|---|---|---|---|
| 2026-11-07 | mesmo vídeo publicado 2× no lives10 em 05/11 ("2.595 cidades"), 06/11 ("Tornado no Brasil") e 07/11 ("Granizo") — dois fluxos chamando publicar com o mesmo vídeo | trava: mesmo canal + mesmo título em 48 h devolve o URL existente (2.5.1) | infra |
| 2026-10-23 | verticais de 3–4 min (Outubro Negro e eMudhra 9:16, lives1 e lives4) saíram sem thumb: todo vídeo em pé era tratado como Short | sem thumb só se vertical E ≤ 180 s; thumbs aplicadas depois com `set_thumb` | infra |
| 2026-10-18 | troquei o campo `thumb` no plano.json para a capa própria e o `publicar --plano` ignorou: aplicou a `thumb_arte.png` do Codex (robô com olhos e androide com rosto) em uK0lVubWsyo e oFSDIzNJmWc | thumb própria vai por `--thumb <jpg>`; corrigidas depois com `set_thumb` | prompt |
