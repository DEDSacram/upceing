// useProducts.js — React Query pattern starter (needs npm install to run in an app).
// Shown here as the canonical shape: query keys, useQuery, useMutation with
// optimistic update + rollback + invalidation. Import { productKeys } from "./queryLogic.js".

// import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
// import { productKeys } from "./queryLogic.js";
//
// export function useProducts(api) {
//   return useQuery({ queryKey: productKeys.all, queryFn: api.list, staleTime: 30_000 });
// }
//
// export function useCreateProduct(api) {
//   const qc = useQueryClient();
//   return useMutation({
//     mutationFn: api.create,
//     onMutate: async (draft) => {
//       await qc.cancelQueries({ queryKey: productKeys.all });
//       const prev = qc.getQueryData(productKeys.all);
//       qc.setQueryData(productKeys.all, (old) => [...(old ?? []), { ...draft, id: -Date.now() }]);
//       return { prev };
//     },
//     onError: (_e, _v, ctx) => qc.setQueryData(productKeys.all, ctx.prev), // rollback
//     onSettled: () => qc.invalidateQueries({ queryKey: productKeys.all }), // refetch truth
//   });
// }
export {};
