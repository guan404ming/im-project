const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : "http://localhost:3000/api";

export default function useInfer() {
  async function getResult(image: File) {
    const formData = new FormData();
    formData.append("file", image);

    const res = await fetch(`${URL}/infer`, {
      method: "POST",
      body: formData
    });
    return await res.json();
  }

  return {
    getResult,
  }
}
