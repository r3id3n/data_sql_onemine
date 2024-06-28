QUERIES_MTBOX = {
"Consulta Loop": 
"""USE MTOnemineClient;
DECLARE @fechaInicio datetimeoffset(7) = '{fechaInicio}';
DECLARE @fechaFin datetimeoffset(7) = '{fechaFin}';
DECLARE @Pala varchar(MAX)
SET @Pala = '{pala}'
--Loop
--Buscar las vueltas realizadas en el equipo, otorgando una descripción de lo realizado
SELECT 
    L.LoopsId,
    L.ServerId,
    CONVERT(VARCHAR(10), L.StartedAt, 120) AS FechaStartedAt, -- 'yyyy-mm-dd'
    CONVERT(VARCHAR(8), L.StartedAt, 108) AS HoraStartedAt,   -- 'HH:MM:SS'
    CONVERT(VARCHAR(10), L.FinishedAt, 120) AS FechaFinishedAt, -- 'yyyy-mm-dd'
    CONVERT(VARCHAR(8), L.FinishedAt, 108) AS HoraFinishedAt,   -- 'HH:MM:SS'
    M.Name AS Equipo,
    L.OperatorId,
    O.FirstName,
    O.LastName,
    Z.Name AS MB,
    S.Name AS Zanja,
    E.Name AS Descarga,
    E.TagId AS TagDesc,
    CONVERT(VARCHAR(10), L.CreatedAt, 120) AS FechaLoopsCreatedAt, -- 'yyyy-mm-dd'
    CONVERT(VARCHAR(8), L.CreatedAt, 108) AS HoraLoopsCreatedAt,   -- 'HH:MM:SS'
    CONVERT(VARCHAR(10), L.UpdatedAt, 120) AS FechaLoopsUpdatedAt, -- 'yyyy-mm-dd'
    CONVERT(VARCHAR(8), L.UpdatedAt, 108) AS HoraLoopsUpdatedAt,   -- 'HH:MM:SS'
    L.RssiExtractionPoint,
    L.RssiDumpPoint,
    L.Valid,
    LOT.Description,
    L.TagId,
    ST.Name AS StatusOper,
    L.TimeDumpToExtractionPoint,
    L.TimeInExtractionPoint,
    L.TimeExtractionToDumpPoint,
    L.TimeInDumpPoint,
    AT.AlgorithmName
FROM 
    Loops L
    INNER JOIN Machines M ON L.MachineId = M.MachinesId
    INNER JOIN Operators O ON L.OperatorId = O.OperatorsId
    INNER JOIN Zones S ON L.StartZoneId = S.ZonesId
    INNER JOIN Zones E ON L.EndZoneId = E.ZonesId
    INNER JOIN LoopOperationType LOT ON L.OperationType = LOT.LoopOperationTypeId
    INNER JOIN Status ST ON L.StatusId = ST.StatusId
    INNER JOIN AlgorithmType AT ON L.AlgorithmTypeId = AT.AlgorithmTypeId
    RIGHT JOIN Zones Z ON S.ParentZoneId = Z.ZonesId
WHERE 
    M.Name = @Pala
    AND L.CreatedAt >= @fechaInicio
    AND L.CreatedAt <= @fechaFin
    AND CONVERT(TIME, L.CreatedAt) BETWEEN CONVERT(TIME, @fechaInicio) AND CONVERT(TIME, @fechaFin)
ORDER BY 
    L.LoopsId DESC;""",
#********************************************************************************************
"Consulta RawData (RSSI)": 
"""USE MTOnemineClient;
DECLARE @fechaInicio datetimeoffset(7) = '{fechaInicio}';
DECLARE @fechaFin datetimeoffset(7) = '{fechaFin}';
--RawData (RSSI)
--Frecuencia RSSI del equipo consultado, buscando la frecuencia en el rango mayor a -80
SELECT 
    RawDatasId,
    RawDatas.TagId,
    b.Name AS MB,
    a.Name AS Zanja,
    AntennaId,
    RSSI,
    CAST (Timestamp AS smalldatetime) AS Timestamp,
    BatteryStatus,
    ObjectType,
    CAST (RawDatas.CreatedAt AS smalldatetime) AS CreatedAt,
    CAST (ReadyToEmitAt AS smalldatetime) AS ReadyToEmitAt
FROM RawDatas
INNER JOIN Zones A ON (RawDatas.TagId = A.TagId)
RIGHT JOIN Zones B ON (A.ParentZoneId = B.ZonesId)
WHERE RawDatas.CreatedAt >= @fechaInicio AND RawDatas.CreatedAt <= @fechaFin 
AND RSSI > -80
ORDER BY RawDatas.CreatedAt DESC;""",
#********************************************************************************************
"Consulta SideSelection (N/S)": 
"""USE MTOnemineClient;
DECLARE @fechaInicio datetimeoffset(7) = '{fechaInicio}';
DECLARE @fechaFin datetimeoffset(7) = '{fechaFin}';
DECLARE @Pala varchar(MAX)
SET @Pala = '{pala}'
--SideSelection
--Selección de zona Norte || Sur del equipo
SELECT DISTINCT
S.SideSelectionLogsId,
S.Side,
S.SessionId,
S.OperatorId,
O.FirstName,
O.LastName,
S.CreatedAt,
S.SideSelectionTypeId
FROM Machines M
INNER JOIN Loops L ON (M.MachinesId = L.MachineId)
LEFT JOIN Operators O ON (O.OperatorsId = L.OperatorId)
RIGHT JOIN SideSelectionLogs S ON (S.OperatorId = O.OperatorsId)
WHERE M.Name = @Pala 
AND S.CreatedAt >= @fechaInicio AND S.CreatedAt <= @fechaFin
ORDER BY S.CreatedAt DESC;""",
#********************************************************************************************
"Consulta MachineStatusLogs (Estado)": 
"""USE MTOnemineClient;
--Registro de estado por Equipo
SELECT 
MSLS.MachineStatusLogsId
,MSLS.ServerId
,MSLS.MachineId
,M.Name AS Machine_Name
,O.OperatorsId
,O.FirstName
,O.LastName
,MSLS.MachineStatusId
,MS.Name AS Status_Name
,MSLS.Timestamp
,MSLS.CreatedAt
FROM MachineStatusLogs MSLS
INNER JOIN MachineStatus AS MS ON (MSLS.MachineStatusId = MS.MachineStatusId) 
INNER JOIN Machines AS M ON(MSLS.MachineId = M.MachinesId)
INNER JOIN Operators AS O ON(MSLS.OperatorId = O.OperatorsId)
AND MSLS.CreatedAt >= @fechaInicio AND MSLS.CreatedAt <= @fechaFin
ORDER BY MSLS.CreatedAt DESC
"""
}