"use client";

import { useRef, useState } from "react";
import Image from "next/image";
import useInfer from "../hooks/use-infer";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Badge } from "@/src/components/ui/badge";

export default function Home() {
  const { getResult } = useInfer();
  const [images, setImages] = useState<any[]>([]);
  const [inputImage, setInputImage] = useState<File | null>(null);

  return (
    <main className="flex justify-center items-start px-12 pb-12 space-x-4">
      <Card className="p-4 space-y-2 h-96">
        <Input
          type="file"
          placeholder="upload some pic"
          onChange={(e) => {
            setInputImage(e.target.files?.[0] as File);
          }}
        />
        <Button
          className="w-full"
          onClick={async () => {
            if (!inputImage) return;
            const res = await getResult(inputImage);
            setImages(res.clean_clothing_images);
          }}
        >
          Submit
        </Button>
        {inputImage && (
          <div className="flex justify-center items-center">
            <Image
              src={URL.createObjectURL(inputImage)}
              alt="upload pic"
              width={200}
              height={200}
            />
          </div>
        )}
      </Card>

      <Card className="grid grid-cols-2 gap-2 min-h-96 w-full p-8">
        {images.map((image, index) => (
          <div
            className="flex flex-col justify-center items-center p-6 space-y-4 border rounded-lg"
            key={index}
          >
            <Image
              key={index}
              src={`data:image/png;base64,${image.image}`}
              alt={`clean clothing ${index}`}
              width={200}
              height={200}
            />
            <div className="flex space-x-2">
              {image.attributes.map((attribute: string, index: number) => (
                <Badge key={index} variant={"outline"} className="text-sm">
                  {attribute}
                </Badge>
              ))}
            </div>
          </div>
        ))}
      </Card>
    </main>
  );
}
