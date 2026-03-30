# 驱动函数分类统计

## 总体统计（去重后，按函数名）

| 分类 | 描述 | 数量 | 占比 |
|------|------|------|------|
| INIT | 外设初始化，影响固件状态机 | 110 | 29.9% |
| LOOP | 轮询等待硬件状态 | 45 | 12.2% |
| NEEDCHECK | 需要进一步分析的函数 | 72 | 19.6% |
| RETURNOK | 硬件操作，返回状态值 | 50 | 13.6% |
| RECV | 从硬件/DMA 读取数据 | 45 | 12.2% |
| IRQ | 中断处理/回调函数 | 14 | 3.8% |
| CORE | 系统区操作，OS 核心函数 | 8 | 2.2% |
| SKIP | 硬件操作，返回 void | 15 | 4.1% |
| NODRIVER | 纯业务逻辑，无需替换 | 9 | 2.4% |
| **合计** | | **368** | **100%** |

## 代表性 Demo 统计（去重后）

| Demo 名称 | INIT | LOOP | NEED | OK | RECV | IRQ | CORE | SKIP | NODR | 总计 |
|-----------|------|------|------|-----|------|-----|------|------|------|------|
| fatfs | 57 | 23 | 7 | 21 | 12 | 2 | 6 | 2 | 0 | 130 |
| LwIP_HTTP_Server_SocketRTOS | 57 | 23 | 7 | 21 | 12 | 2 | 6 | 2 | 0 | 130 |
| LwIP_StreamingServer | 57 | 23 | 7 | 21 | 12 | 2 | 6 | 2 | 0 | 130 |
| LwIP_HTTP_Server_Socket_RTOS | 42 | 16 | 11 | 24 | 15 | 6 | 2 | 4 | 2 | 122 |
| LwIP_HTTP_Server_Raw | 38 | 15 | 5 | 3 | 20 | 5 | 1 | 1 | 0 | 88 |
| UART_Hyperterminal_IT | 23 | 12 | 4 | 11 | 19 | 6 | 2 | 2 | 0 | 79 |
| NXP_UART_BareMetal | 1 | 0 | 27 | 1 | 0 | 0 | 0 | 0 | 1 | 30 |
| NXP_UART_FreeRTOS | 13 | 5 | 0 | 1 | 8 | 2 | 0 | 1 | 0 | 30 |
| i2c | 11 | 2 | 3 | 1 | 4 | 0 | 0 | 0 | 3 | 24 |
| NXP_I2C_BareMetal | 4 | 0 | 15 | 1 | 1 | 0 | 0 | 0 | 1 | 22 |

## 各类别函数名清单


### INIT - 外设初始化，影响固件状态机

**数量**: 110

```
BOARD_BootClockRUN
BOARD_BootClockRUN_528M
BSP_COM_Init
BSP_LCD_Init
BSP_LCD_MspInit
BSP_LED_Init
BSP_PB_Init
BSP_POTENTIOMETER_Init
BSP_SDRAM_MspInit
BSP_SD_MspInit
BSP_SRAM_MspInit
CLOCK_InitArmPll
CLOCK_InitAudioPll
CLOCK_InitEnetPll
CLOCK_InitExternalClk
CLOCK_InitSysPll
CLOCK_InitUsb1Pll
CLOCK_InitUsb2Pll
CLOCK_InitVideoPll
CLOCK_SetDiv
CLOCK_SetMux
ENET_AddMulticastGroup
ENET_SetMacController
ETH_DMARxDescListInit
ETH_DMATxDescListInit
ETH_Prepare_Tx_Descriptors
FLASH_FlushCaches
FSMC_BANK3_MspInit
HAL_ADCEx_InjectedStart
HAL_ADCEx_InjectedStart_IT
HAL_ADCEx_MultiModeStart_DMA
HAL_ADC_ConfigChannel
HAL_ADC_MspInit
HAL_ADC_Start
HAL_ADC_Start_DMA
HAL_ADC_Start_IT
HAL_DCMI_Start_DMA
HAL_DMA_Init
HAL_DSI_DeInit
HAL_DSI_EnterULPM
HAL_DSI_EnterULPMData
HAL_DSI_Init
HAL_DSI_Start
HAL_DSI_Stop
HAL_ETH_Init
HAL_ETH_MspInit
HAL_ETH_SetWakeUpFilter
HAL_ETH_WritePHYRegister
HAL_FLASHEx_Erase
HAL_GPIO_DeInit
HAL_GPIO_Init
HAL_I2C_Master_Receive_DMA
HAL_I2C_Master_Receive_IT
HAL_I2C_Master_Seq_Receive_IT
HAL_I2C_Master_Seq_Transfer_DMA
HAL_I2C_Master_Seq_Transmit_IT
HAL_I2C_Master_Transmit_DMA
HAL_I2C_Master_Transmit_IT
HAL_I2C_Mem_Read_IT
HAL_I2C_Mem_Write_IT
HAL_I2C_Slave_Seq_Receive_IT
HAL_I2C_Slave_Seq_Transmit_IT
HAL_LTDC_DeInit
HAL_MspInit
HAL_PWREx_ControlVoltageScaling
HAL_PWREx_DisableBkUpReg
HAL_PWREx_DisableOverDrive
HAL_PWREx_EnableBkUpReg
HAL_PWREx_EnableOverDrive
HAL_PWREx_EnterUnderDriveSTOPMode
HAL_RCCEx_DisablePLLI2S
HAL_RCCEx_EnablePLLI2S
HAL_RCCEx_EnablePLLSAI
HAL_RCCEx_PeriphCLKConfig
HAL_RCC_ClockConfig
HAL_RCC_DeInit
HAL_RCC_MCOConfig
HAL_RCC_OscConfig
HAL_SPI_MspInit
HAL_TIMEx_HallSensor_DeInit
HAL_TIMEx_HallSensor_Stop_DMA
HAL_TIMEx_HallSensor_Stop_IT
HAL_TIMEx_OCN_Stop_IT
HAL_TIMEx_OnePulseN_Stop
HAL_TIMEx_OnePulseN_Stop_IT
HAL_TIM_Base_DeInit
HAL_TIM_Base_MspInit
HAL_TIM_Encoder_DeInit
HAL_TIM_Encoder_Stop_DMA
HAL_TIM_IC_DeInit
HAL_TIM_IC_Stop_IT
HAL_TIM_MspPostInit
HAL_TIM_OC_DeInit
HAL_TIM_OC_Stop_DMA
HAL_TIM_OC_Stop_IT
HAL_TIM_OnePulse_DeInit
HAL_TIM_PWM_DeInit
HAL_TIM_PWM_Stop_IT
HAL_UART_Abort
HAL_UART_AbortTransmit_IT
HAL_UART_MspInit
I2Cx_ITConfig
I2Cx_MspInit
LPUART_Deinit
LPUART_Init
SystemClock_Config
UART_SetConfig
UART_Start_Receive_DMA
rt_hw_pin_init
rt_hw_spi_bus_init
```

### LOOP - 轮询等待硬件状态

**数量**: 45

```
CLOCK_SetDiv
CLOCK_SetMux
DSI_ShortWrite
ENET_MDIOWaitTransferOver
FLASH_WaitForLastOperation
HAL_ADCEx_InjectedPollForConversion
HAL_ADC_PollForConversion
HAL_ADC_PollForEvent
HAL_DCMI_Stop
HAL_DCMI_Suspend
HAL_DMA2D_Abort
HAL_DMA2D_CLUTLoading_Abort
HAL_DMA2D_CLUTLoading_Suspend
HAL_DMA2D_PollForTransfer
HAL_DMA2D_Suspend
HAL_DMA_Abort
HAL_DSI_ExitULPM
HAL_DSI_ExitULPMData
HAL_ETH_ReleaseTxPacket
HAL_I2C_IsDeviceReady
HAL_I2C_Mem_Write
HAL_PWREx_ControlVoltageScaling
HAL_PWREx_DisableBkUpReg
HAL_PWREx_EnableBkUpReg
HAL_RCCEx_DisablePLLI2S
HAL_RCCEx_DisablePLLSAI
HAL_RCC_DeInit
I2C_DMAAbort
I2C_RequestMemoryRead
I2C_RequestMemoryWrite
I2C_WaitOnBTFFlagUntilTimeout
I2C_WaitOnFlagUntilTimeout
I2C_WaitOnMasterAddressFlagUntilTimeout
I2C_WaitOnRXNEFlagUntilTimeout
I2C_WaitOnSTOPFlagUntilTimeout
I2C_WaitOnSTOPRequestThroughIT
I2C_WaitOnTXEFlagUntilTimeout
I2C_WaitOnTXISFlagUntilTimeout
LPI2C_MasterStop
LPI2C_MasterWaitForTxFifoAllEmpty
LPUART_WaitForReadData
LPUART_WriteBlocking
LPUART_WriteBlocking16bit
LPUART_WriteNonBlocking
UART_WaitOnFlagUntilTimeout
```

### NEEDCHECK - 需要进一步分析的函数

**数量**: 72

```
BOARD_BootClockRUN
BOARD_BootClockRUN_528M
BOARD_ReconfigFlexSpiRxBuffer
CLOCK_InitArmPll
CLOCK_InitAudioPll
CLOCK_InitEnetPll
CLOCK_InitExternalClk
CLOCK_InitSysPll
CLOCK_InitUsb1Pll
CLOCK_InitUsb2Pll
CLOCK_InitVideoPll
CLOCK_SetDiv
CLOCK_SetMux
ENET_AddMulticastGroup
ENET_GetInstance
ENET_GetRxFrame
ENET_LeaveMulticastGroup
ENET_ReceiveIRQHandler
ENET_SetMacController
ENET_TransmitIRQHandler
ETH_Prepare_Tx_Descriptors
ETH_UpdateDescriptor
GPIO_GetInstance
HAL_FLASHEx_Erase
HAL_I2C_IsDeviceReady
HAL_I2C_Master_Transmit
HAL_RCC_ClockConfig
HAL_RCC_DeInit
HAL_SPI_MspInit
HAL_TIMEx_HallSensor_Stop_DMA
HAL_TIMEx_PWMN_Stop_IT
HAL_TIM_Base_Stop_DMA
HAL_TIM_Encoder_Stop_IT
HAL_TIM_MspPostInit
HAL_TIM_OnePulse_Stop_IT
HAL_TIM_PWM_Stop
HAL_TIM_PWM_Stop_DMA
HAL_UART_AbortReceive
HAL_UART_AbortReceive_IT
HAL_UART_Abort_IT
I2C_DMAAbort
I2C_IsErrorOccurred
I2C_MasterRequestRead
I2C_RequestMemoryRead
LPI2C_GetInstance
LPI2C_MasterReceive
LPI2C_MasterSend
LPI2C_MasterStop
LPI2C_MasterWaitForTxReady
LPI2C_SlaveReceive
LPI2C_SlaveSend
LPI2C_TransferStateMachineSendCommand
LPUART_Deinit
LPUART_Init
LPUART_ReadBlocking
LPUART_ReadBlocking16bit
LPUART_ReadNonBlocking
LPUART_ReadNonBlocking16bit
LPUART_SetBaudRate
LPUART_TransferHandleIDLEReady
LPUART_TransferHandleReceiveDataFull
LPUART_TransferHandleSendDataEmpty
LPUART_TransferReceiveNonBlocking
LPUART_WaitForReadData
LPUART_WriteBlocking
LPUART_WriteBlocking16bit
LPUART_WriteNonBlocking
LPUART_WriteNonBlocking16bit
UART_EndTxTransfer
imxrt_isr
rt_hw_pin_init
rt_hw_spi_bus_init
```

### RETURNOK - 硬件操作，返回状态值

**数量**: 50

```
BSP_LCD_DisplayChar
BSP_LCD_GetXSize
CLOCK_SetDiv
ENET_AddMulticastGroup
ENET_LeaveMulticastGroup
HAL_ETH_ReadPHYRegister
HAL_ETH_SetWakeUpFilter
HAL_ETH_WritePHYRegister
HAL_GPIO_DeInit
HAL_GPIO_Init
HAL_I2CEx_DisableFastModePlus
HAL_I2CEx_EnableFastModePlus
HAL_I2C_IsDeviceReady
HAL_LIN_SendBreak
HAL_MultiProcessor_EnterMuteMode
HAL_MultiProcessor_ExitMuteMode
HAL_RCC_MCOConfig
HAL_TIMEx_HallSensor_Stop
HAL_TIMEx_HallSensor_Stop_IT
HAL_TIMEx_OCN_Stop
HAL_TIMEx_OCN_Stop_DMA
HAL_TIMEx_OCN_Stop_IT
HAL_TIMEx_OnePulseN_Stop
HAL_TIMEx_OnePulseN_Stop_IT
HAL_TIMEx_PWMN_Stop
HAL_TIMEx_PWMN_Stop_DMA
HAL_TIM_Base_Stop
HAL_TIM_Base_Stop_IT
HAL_TIM_Encoder_Stop
HAL_TIM_Encoder_Stop_DMA
HAL_TIM_Encoder_Stop_IT
HAL_TIM_IC_Stop
HAL_TIM_IC_Stop_DMA
HAL_TIM_IC_Stop_IT
HAL_TIM_OC_DeInit
HAL_TIM_OC_Stop
HAL_TIM_OC_Stop_DMA
HAL_TIM_OC_Stop_IT
HAL_TIM_OnePulse_Stop
HAL_TIM_OnePulse_Stop_IT
HAL_TIM_PWM_Stop_IT
HAL_UART_AbortTransmit
HAL_UART_DMAPause
HAL_UART_DMAResume
HAL_UART_DMAStop
I2C_MasterRequestRead
LPI2C_MasterSetBaudRate
LPUART_GetInstance
LPUART_SetBaudRate
UART_EndRxTransfer
```

### RECV - 从硬件/DMA 读取数据

**数量**: 45

```
ENET_GetRxFrame
HAL_ADCEx_MultiModeStart_DMA
HAL_DSI_LongWrite
HAL_DSI_Read
HAL_ETH_ReadData
HAL_ETH_ReadPHYRegister
HAL_ETH_Transmit
HAL_ETH_Transmit_IT
HAL_I2C_Master_Receive
HAL_I2C_Master_Receive_DMA
HAL_I2C_Master_Receive_IT
HAL_I2C_Master_Seq_Receive_DMA
HAL_I2C_Master_Seq_Receive_IT
HAL_I2C_Master_Seq_Transfer_DMA
HAL_I2C_Master_Transmit
HAL_I2C_Master_Transmit_DMA
HAL_I2C_Mem_Read
HAL_I2C_Mem_Read_DMA
HAL_I2C_Mem_Read_IT
HAL_I2C_Mem_Write
HAL_I2C_Mem_Write_DMA
HAL_I2C_Slave_Receive
HAL_I2C_Slave_Seq_Receive_DMA
HAL_I2C_Slave_Seq_Transmit_DMA
HAL_I2C_Slave_Transmit
HAL_UARTEx_ReceiveToIdle
HAL_UARTEx_ReceiveToIdle_DMA
HAL_UARTEx_ReceiveToIdle_IT
HAL_UART_Receive
HAL_UART_Transmit
HAL_UART_Transmit_DMA
LPI2C_MasterReceive
LPI2C_MasterSend
LPI2C_RunTransferStateMachine
LPI2C_SlaveReceive
LPUART_ReadBlocking
LPUART_ReadBlocking16bit
LPUART_ReadNonBlocking
LPUART_ReadNonBlocking16bit
LPUART_TransferHandleReceiveDataFull
LPUART_TransferReceiveNonBlocking
LPUART_WriteNonBlocking16bit
UART_Receive_IT
imxrt_i2c_mst_xfer
uart_task
```

### IRQ - 中断处理/回调函数

**数量**: 14

```
ENET_ReceiveIRQHandler
ENET_TransmitIRQHandler
HAL_DMA_IRQHandler
HAL_ETH_IRQHandler
HAL_GpioInterruptHandle
HAL_TIMEx_PWMN_Stop_IT
HAL_UART_IRQHandler
I2C_Master_ADDR
I2C_Slave_ADDR
I2C_Slave_STOPF
LPUART_TransferHandleIDLEReady
LPUART_TransferHandleSendDataEmpty
UART_DMAReceiveCplt
UART_DMATransmitCplt
```

### CORE - 系统区操作，OS 核心函数

**数量**: 8

```
BSP_CAMERA_MspInit
BSP_PB_Init
BSP_SRAM_MspInit
HAL_InitTick
HAL_UART_MspInit
I2Cx_ITConfig
I2Cx_MspInit
MFX_IO_ITConfig
```

### SKIP - 硬件操作，返回 void

**数量**: 15

```
BSP_LCD_DisplayStringAt
BSP_LCD_DisplayStringAtLine
BSP_LCD_Reset
BSP_LCD_SetTextColor
CLOCK_SetDiv
FLASH_FlushCaches
HAL_ADC_MspInit
HAL_GPIO_DeInit
HAL_MspInit
HAL_RCC_MCOConfig
HAL_TIM_Base_MspInit
HAL_TIM_PWM_Stop
HAL_TIM_PWM_Stop_DMA
HAL_UART_MspInit
LPUART_GetInstance
```

### NODRIVER - 纯业务逻辑，无需替换

**数量**: 9

```
BSP_LCD_DrawPixel
BSP_LCD_GetFont
DMAMUX_GetInstance
EDMA_GetInstance
ENET_GetInstance
GPIO_GetInstance
HAL_MspInit
LPI2C_GetInstance
main
```
