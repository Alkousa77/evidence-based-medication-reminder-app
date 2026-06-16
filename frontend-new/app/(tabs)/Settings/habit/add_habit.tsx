import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useState} from "react";
import api from "@/lib/api";
import { useRouter } from "expo-router";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import validator from "validator";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
//enable parsing for custom format "HH:mm"
dayjs.extend(customParseFormat);

export default function AddHabit(){

    const[name, setName] = useState<string>("");
    const[time, setTime] = useState<string>("");
    const router = useRouter();

    //Create
    const createHabit = async ()=>{
    
        if(validator.isEmpty(name.trim())){
            alert("Habit name is required");
            return;
        }
        if(validator.isEmpty(time.trim())){
            alert("Habit time is required");
            return;
        }  
        //validate time format strict mode = true (24 hour format)
        if(!dayjs(time, "HH:mm", true).isValid()){
            alert("Time must be in HH:mm format");
            return;
        }
        try {
            await api.post("/habits", {name, time});
            router.push("/(tabs)/Settings/habit")
        } catch (error) {
            console.log("failed to create habit");
        }
    };

    return (
                <ScreenWrapper>
                <ScreenHeader title="Add Habit"></ScreenHeader>
                <AppInput
                label="Habit Name"
                value={name}
                onChangeText={setName}
                placeholder="Breakfast"
                />
                <AppInput
                label="Habit Time"
                value={time}
                onChangeText={setTime}
                placeholder="09:00"
                />
                <ButtomButtonContainer>
                <AppButton
                title="Add Habit" onPress={createHabit}
                />
                </ButtomButtonContainer>      
                </ScreenWrapper>
    );
}