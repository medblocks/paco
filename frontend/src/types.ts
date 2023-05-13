import { env } from "$env/dynamic/public";
import { io } from "socket.io-client";

export const DoctorSocket = io(`${env.PUBLIC_SERVER_URL}`);

export interface TranscriptMessage{
    speaker: number | string;
    text: string;
};