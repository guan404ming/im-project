const URL = "http://127.0.0.1:5328/api";

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
