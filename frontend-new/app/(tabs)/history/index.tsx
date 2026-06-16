import {View, Text, TextInput, FlatList} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import { ListItem } from "@/components/list-item-card";
import { useCallback, useEffect, useState } from "react";
import api from "@/lib/api";
import { StatusBadge } from "@/components/status-badge";
import {format} from "date-fns";
import { useFocusEffect } from "expo-router";

type Status = "Taken" | "Missed"
type Log = {id:number, status:Status, scheduled_date:string,medication:string}

export default function Logs() {
    const [logs, setLogs] = useState<Log[]>([]);

    //fetch
    const fetchLogs = async ()=>{
        try {
            const res = await api.get("/doses/logs");
            setLogs(res.data)
        } catch (error) {
            console.log("error fetching logs");
        }
    };

        //refetch logs whn screen in focus
        useFocusEffect( 
            useCallback(()=>{
            fetchLogs();
        },[]))

    return(
        <ScreenWrapper>
        <ScreenHeader title = "Dose History" showBackArrow={false}/>
        <FlatList
        data={logs}
        keyExtractor={(item)=>item.id.toString()}
        renderItem={({item})=>(
            <ListItem
            direction="column"
            title={item.medication}
            subtitle={format(new Date(item.scheduled_date), "EEE, MMM d, yyyy 'at' HH:mm")}
            right={
            <StatusBadge status={item.status}/>}
            ></ListItem>
        )}
        />

        </ScreenWrapper>
    )
}