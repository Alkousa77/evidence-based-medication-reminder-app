import {View, Text, TouchableOpacity,ScrollView} from "react-native";
import {useEffect, useState} from "react";
import DateTimePicker from "@react-native-community/datetimepicker"
import api from "@/lib/api"
import { useLocalSearchParams, useRouter } from "expo-router";
import { AppButton } from "@/components/app-button";
import ScreenWrapper from "@/components/ScreenWrapper";
import ScreenHeader from "@/components/ScreenHeader";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import { SegmentedButtons } from "react-native-paper";
import DateTimePickerModal from "react-native-modal-datetime-picker";

export default function ScheduleScreen(){
    const [mode, setMode] = useState<"standard"|"habit">("standard");
    const [times, setTimes] = useState<string[]>([]);
    const [days, setDays] = useState<string[]>([]);
    const [showPicker, setShowPicker] = useState(false);
    const [habits, setHabits] = useState<any[]>([]);
    const [selectedHabit, setSelectedHabit] = useState<number | null>(null);
    const [ScheduleSaved, setScheduleSaved] = useState(false);
    const weekDays = ["MON","TUE","WED","THU","FRI","SAT","SUN"]

    const {medication_id} = useLocalSearchParams();
    const router = useRouter();   

    const getHabits = async () => {
        try {
            const res = await api.get("/habits");
            setHabits(res.data);

        } catch (error) {
            alert("failed to fetch habits")
        }
    };
    
    useEffect(()=>{  
        if (!medication_id){
        alert("No med selected")
        router.back();
        return;
        }
   },[]);


   useEffect(() =>{
    if (mode==="habit"){
        getHabits();
    }
   },[mode])
   
    const createSchedule = async () => {
        if (mode=== "standard" && (times.length === 0 || days.length === 0)){
            return alert("Add at least one time and one day");
        }
        if (mode==="habit" && !selectedHabit){
            return alert("Select a habit");
        }
        try {
            const payload = {
                medication_id:Number(medication_id), 
                days: mode === "standard" ? days: [],
                times: mode === "standard"? times: [],
                habit_id: mode === "habit"? selectedHabit:null  
            };
            await api.post("/schedules", payload);
            setScheduleSaved(true);
            alert("schedule Created");
            router.push("/(tabs)/meds");
        } catch (error) {
            alert("Error creating schedule")
        }
    } 

    const cancelSchedule = async () => {
        if (!ScheduleSaved && medication_id){
         await api.delete(`/medications/${medication_id}`)
        }
        router.replace("/(tabs)/meds");
    }
   
    return(
    
        <ScreenWrapper>
            <ScreenHeader title=" Schedule Setup"/>
            <ScrollView
            keyboardShouldPersistTaps="handled"
            contentContainerStyle={{paddingBottom:100}}>
            <SegmentedButtons
            value={mode}
            onValueChange={(val) =>setMode(val as "standard"|"habit")}
            buttons={[
                {value:"standard", label:"Standard", style:{borderRadius:15}},
                {value:"habit", label:"Habit_based", style:{borderRadius:15}}
            ]}
            style={{margin:16, }}
            theme={{colors:{secondaryContainer:"#82b6fa"}}}
            />

            {mode=== "standard" && (
                <>
                <AppButton 
                onPress={()=> setShowPicker(true)}
                title="Select Time"
                />

                {showPicker && (
                    <DateTimePickerModal
                    isVisible= {showPicker}
                    mode="time"
                    locale = "en_GB"
                    is24Hour={true}
                    onConfirm={(date)=> {
                        setShowPicker(false);
                        if(date){
                            const hours = date.getHours().toString().padStart(2, "0");
                            const minutes = date.getMinutes().toString().padStart(2,"0");
                            const formatted = `${hours}:${minutes}`;

                            if (!times.includes(formatted)){
                                setTimes(prev => [...prev, formatted]);
                            }
                        }
                    }}
                    onCancel={()=>setShowPicker(false)}
                    />
                )}

            {/*view list of times*/}
            <View style={{marginTop: 20}}>
                <Text style={{fontWeight:600}}>Daily Times:</Text>
                {times.map((time)=> (
                    <View
                    key={time}
                    style={{flexDirection:"row", justifyContent:"space-between", marginVertical:5, alignItems:"center"}}
                    >
                        <View><Text>{time}</Text></View>
                        <AppButton
                        color="#c04141"
                        title="Delete"
                        onPress={()=>setTimes(prev => prev.filter((current)=> current !==time))}/> 
                    </View>
                ))}
            </View>

            {/*Days*/}
            <Text style={{marginTop:20, fontWeight:600}}>Repeat On:</Text> 
            <View style={{flexDirection:"row", flexWrap: "wrap"}}>

            {weekDays.map(day => ( //index not needed (unique values)
                <TouchableOpacity
                key={day}
                onPress={()=> {
                    if (days.includes(day)){
                        setDays(prev => prev.filter(d => d !== day)) // unselect if already selcted
                    }else{ setDays(prev => [...prev, day])} // add if not selected
                }}
                style={{margin:5, padding:8, 
                    borderWidth:1.5, borderRadius:50,
                    minWidth:40,alignItems:"center",
                    backgroundColor: days.includes(day) ? "#3687b3":"#e7e7e7",
                    borderColor:days.includes(day) ?"#3687b3":"#fff" }}
                ><Text style={{color: days.includes(day) ? "#ffffff":"#5e5c5c",}}>{day}</Text></TouchableOpacity>        
            ))}
            </View>   
            </>
            )}

            {/*Habit Mode*/}
            {mode === "habit" &&(
            <>
                <Text style={{fontWeight:600}}>Link to Habit</Text>
               {habits.map(habit => (
                <TouchableOpacity
                key={habit.id}
                onPress={()=> setSelectedHabit(habit.id)}
                style={{padding:10,
                    borderWidth:1,
                    borderRadius:16,
                    marginVertical:5,
                    backgroundColor: selectedHabit === habit.id? "#3d7fdb": "white"
                }}>
                <Text
                style={{color: selectedHabit === habit.id ? "white": "black"}}
                >{`${habit.name}  ${habit.time}`}
                </Text>
                </TouchableOpacity>
               ))}
            </>
            )}
            </ScrollView>
           <ButtomButtonContainer>
            {/*Save*/}
            <AppButton
            title="Save"
            onPress={createSchedule}
            />
            <AppButton
            title="Cancel"
            color="#d14848"
            onPress={cancelSchedule}
            />
            </ButtomButtonContainer>

        </ScreenWrapper>
    );
}