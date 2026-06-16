import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useEffect, useState} from "react";
import api from "@/lib/api";
import { useLocalSearchParams, useRouter } from "expo-router";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import validator from "validator";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";

dayjs.extend(customParseFormat);

export default function EditHabits(){

    const[name, setName] = useState<string>("");
    const[time, setTime] = useState<string>("");
    const {habit_id} = useLocalSearchParams();
    const router = useRouter();
    
    //fetch 
    const getHabit = async  ()=>{
        try {
            const res = await api.get(`/habits/me/${habit_id}`)
            setName(res.data.name);
            setTime(res.data.time);
        } catch (error) {
            alert("No Habit Passed")
        }
    }
    useEffect(()=>{
        getHabit();
    }, [])

    //Update
    const updateHabit = async ()=>{
        if(validator.isEmpty(name.trim())){
            alert("Habit name is required");
            return;
        }
        if(validator.isEmpty(time.trim())){
            alert("Habit time is required");
            return;
        }  
        if(!dayjs(time, "HH:mm", true).isValid()){
            alert("Time must be in HH:mm format");
            return;
        }
        try {
            await api.put("/habits", {id: habit_id,name, time});
            router.push("/(tabs)/Settings/habit");
        } catch (error) {
            console.log("failed to update habit");
        }
    };

    return (
                <ScreenWrapper>
                <ScreenHeader title="Edit Habit"></ScreenHeader>
                <AppInput
                label="Habit Name"
                value={name}
                onChangeText={setName}
                />
                <AppInput
                label="Habit Time"
                value={time}
                onChangeText={setTime}
                />
                <ButtomButtonContainer>
                <AppButton
                title="Update Habit" onPress={updateHabit}
                />
                </ButtomButtonContainer>
                </ScreenWrapper>
    );
}