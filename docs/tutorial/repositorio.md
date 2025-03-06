# Paso 3: Repositorio

## Clona el repositorio


```powershell
git clone git@github.com:misaelnieto/itm_2025_soa_u2.git
cd itm_2025_soa_u2
git switch --create fferndez-servicioweb
```

## Crea tu rama de trabajo

De preferencia, usa el nombre de tu módulo y tu servicio web para darle un
nombre a tu rama. Por ejemplo, si tu módulo de trabajo es `ffernandez` y tu
servicio web se llama `Perritos`, tu rama se podría llamar
`ffernandez-perritos`. Usa `git switch` para crear tu rama y cambiarte a ella.

```powershell
git switch --create ffernandez-perritos
```

Luego registra tu rama en github:

```powershell
git push --set-upstream origin ffernandez-perritos
```

A partir de ahora solamente tendrás que escribir `git push` para subir los
cambios de tu rama a github.
