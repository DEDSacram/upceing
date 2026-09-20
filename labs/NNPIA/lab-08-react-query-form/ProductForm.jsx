// ProductForm.jsx — React Hook Form pattern starter (needs npm install to run).
// Uncontrolled inputs + schema-ish validation + server-error mapping.

// import { useForm } from "react-hook-form";
//
// export function ProductForm({ onSubmit, serverError }) {
//   const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
//     defaultValues: { name: "", price: 0 },
//   });
//   return (
//     <form onSubmit={handleSubmit(onSubmit)}>
//       <input {...register("name", { required: "name is required", maxLength: { value: 100, message: "max 100 chars" } })} />
//       {errors.name && <p>{errors.name.message}</p>}
//       <input type="number" {...register("price", { min: { value: 0, message: "price >= 0" }, valueAsNumber: true })} />
//       {errors.price && <p>{errors.price.message}</p>}
//       {serverError && <p role="alert">{serverError}</p>}
//       <button disabled={isSubmitting}>{isSubmitting ? "saving…" : "save"}</button>
//     </form>
//   );
// }
export {};
