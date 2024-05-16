"use client";

import { useRef, useState } from "react";
import Image from "next/image";
import useInfer from "../hooks/use-infer";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";

export default function Home() {
  const inputRef = useRef<HTMLInputElement>(null);
  const { getResult } = useInfer();
  const [images, setImages] = useState<any[]>([]);

  return (
    <div className="flex-col flex text-center space-y-4 p-8">
      <h1 className="text-3xl font-bold">✨ im-project ✨</h1>
      <Input type="file" placeholder="upload some pic" ref={inputRef}></Input>
      <Button
        onClick={async () => {
          if (!inputRef.current?.files?.[0]) return;
          const res = await getResult(inputRef.current?.files?.[0] as File);
          setImages(res.clean_clothing_images)
        }}
      >
        Submit
      </Button>
      <div className="grid grid-cols-2 gap-2">
        {
          inputRef.current?.files?.[0] && (
            <Card>
              <Image
                src={URL.createObjectURL(inputRef.current?.files?.[0])}
                alt="upload pic"
                width={200}
                height={200}
              />
            </Card>
          )
        }
        {images.map((image, index) => (
          <Image
            key={index}
            src={`data:image/png;base64,${image}`}
            alt={`clean clothing ${index}`}
            width={200}
            height={200}
          />
        ))}
      </div>
    </div>
  );
}
