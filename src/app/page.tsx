import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Home() {
  return (
    <Card className="flex-col flex text-center space-y-4 p-8">
      <h1 className="text-3xl font-bold">✨ im-project ✨</h1>
      <Input type="file" placeholder="upload some pic"></Input>
    </Card>
  );
}
