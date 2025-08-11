# TCE

Existem anotações da versão do ANIA/TCE que não se aplicam ao Tilene. Foram guardados para fins de registro.

## Ambientes TCE-ANIA

| Ambiente        |                   _Hostname_                    | _URL_                                 |
| --------------- | :---------------------------------------------: | ------------------------------------- |
| Desenvolvimento | tst-wa-chatgpt.lnx.tce.sp.gov.br<br>10.26.0.124 | https://chatgpt.desenv.tce.sp.gov.br/ |
| Produção        | pro-wab-ania.lnx.tce.sp.gov.br<br>10.26.191.70  | https://ania.tce.sp.gov.br/           |

<br>

---

## Processamento do PDF

Caso seja necessário fazer limpeza do texto, mudar tamanho dos _chunks_ etc. Utilize o programa:

```shell
./ania/outros_modulos/indexar_arquivos.py
```

A quantidade de _chunks_ enviadas está no arquivo `/opt/PrototipoChatGPT/PrototipoChatGPT/app.py` (pesquisar/pesquisar_documento).

<br>

---

## Inclusão ou alteração dos exemplos

Estes são os textos que aparecem em _ANIA.legis_ e possuem `id_usuario=NULL` na tabela de textos.

```sql
SELECT id, id_usuario, arquivo, texto, num_tokens, embedding
FROM public.textos
WHERE id_usuario is null;
```

Para incluir um novo arquivo, siga o procedimento:

- Use o próprio sistema e faça o _upload_ do arquivo com seu próprio usuário.
- Selecionar os textos pelo _id_usuario_ e arquivo na tabela textos e substituir o id_usuario destes registros por NULL.
- Incluir o arquivo PDF em `/opt/ANIA/arquivos/exemplos` (no caso do teste).
- Testar o funcionamento no sistema e verificar se o link para o arquivo também funciona.
