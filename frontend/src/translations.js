// Translation files for multi-language support
export const translations = {
  en: {
    common: {
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      cancel: 'Cancel',
      confirm: 'Confirm',
      close: 'Close',
      save: 'Save',
      edit: 'Edit',
      delete: 'Delete',
      back: 'Back',
      next: 'Next',
      previous: 'Previous',
      submit: 'Submit',
      reset: 'Reset',
      search: 'Search',
      filter: 'Filter',
      sort: 'Sort',
      refresh: 'Refresh',
      download: 'Download',
      upload: 'Upload',
      print: 'Print',
      share: 'Share',
      copy: 'Copy',
      paste: 'Paste',
      cut: 'Cut',
      select: 'Select',
      selectAll: 'Select All',
      clear: 'Clear',
      apply: 'Apply',
      ok: 'OK',
      yes: 'Yes',
      no: 'No'
    },
    
    navigation: {
      home: 'Home',
      about: 'About',
      contact: 'Contact',
      help: 'Help',
      settings: 'Settings',
      profile: 'Profile',
      logout: 'Logout',
      login: 'Login',
      register: 'Register',
      dashboard: 'Dashboard',
      reports: 'Reports',
      admin: 'Admin',
      candidate: 'Candidate'
    },
    
    landing: {
      title: 'Elite AI Interview Platform',
      subtitle: 'Experience the future of hiring with our advanced AI-powered interview system. Features interactive coding challenges, empathetic candidate workflow, multi-vector assessments, and comprehensive bias mitigation controls.',
      features: {
        codingChallenges: 'Interactive Coding Challenges',
        voiceInterview: 'Voice Interview with AI',
        multiVectorAssessment: 'Multi-Vector Assessments',
        biasMitigation: 'Bias Mitigation Controls'
      },
      adminPortal: {
        title: 'Admin Dashboard',
        description: 'Comprehensive hiring management with candidate pipeline, interview customization, coding challenges, and advanced multi-vector reporting with bias controls.',
        features: {
          candidatePipeline: 'Candidate Pipeline & Comparison Tools',
          roleArchetypes: 'Role Archetypes & Interview Focus',
          codingChallenges: 'Interactive Coding Challenges'
        },
        button: 'Access Admin Portal'
      },
      candidatePortal: {
        title: 'Candidate Experience',
        description: 'Interactive and empathetic interview experience with guided setup, practice rounds, question controls, and adaptive AI questioning for a fair assessment.',
        features: {
          setupCheck: 'Camera/Mic Check & Practice Round',
          questionCards: 'Question Cards with Thinking Time',
          interactiveModules: 'Interactive Modules & Coding Tasks'
        },
        button: 'Start Interview Experience'
      },
      placementPreparation: {
        title: 'Placement Preparation',
        description: 'Comprehensive placement preparation tools with interview creation, practice sessions, and skill assessment to help you prepare for your dream job.',
        features: {
          createInterview: 'Create Custom Interviews',
          practiceRounds: 'Practice & Mock Sessions',
          skillAssessment: 'Skill Assessment Tools'
        },
        button: 'Start Preparation'
      }
    },
    
    auth: {
      adminLogin: {
        title: 'Admin Login',
        subtitle: 'Enter your admin credentials to continue',
        passwordLabel: 'Admin Password',
        passwordPlaceholder: 'Enter admin password',
        loginButton: 'Login',
        loggingIn: 'Logging in...',
        backToHome: 'Back to Home',
        errors: {
          invalidPassword: 'Invalid password',
          connectionError: 'Connection error'
        }
      },
      candidateLogin: {
        title: 'Candidate Portal',
        subtitle: 'Enter your interview token to begin',
        tokenLabel: 'Interview Token',
        tokenPlaceholder: 'Enter your interview token',
        startButton: 'Start Interview',
        starting: 'Starting...',
        backToHome: 'Back to Home',
        errors: {
          invalidToken: 'Invalid token',
          connectionError: 'Connection error'
        }
      }
    },
    
    interview: {
      setup: {
        title: 'Interview Setup',
        subtitle: 'Let\'s prepare for your interview',
        cameraCheck: 'Camera Check',
        microphoneCheck: 'Microphone Check',
        voiceMode: 'Voice Mode',
        textMode: 'Text Mode',
        practiceRound: 'Practice Round',
        ready: 'Ready to Start',
        startInterview: 'Start Interview'
      },
      
      captureImage: {
        title: 'Capture Image',
        subtitle: 'Please position yourself in front of the camera for face verification',
        instructions: {
          camera: 'Make sure your camera is visible and working',
          position: 'Position your face in the center of the guide',
          lighting: 'Ensure good lighting for better detection'
        },
        status: {
          noFace: 'No face detected',
          multipleFaces: 'Multiple faces detected',
          faceDetected: 'Face detected successfully',
          improveLighting: 'Improve the lighting'
        },
        buttons: {
          captureface: 'Capture Face',
          faceCaptured: '✓ Face Captured',
          confirmInterview: 'Confirm Interview',
          retryCamera: 'Retry Camera Access'
        }
      },
      
      questions: {
        questionNumber: 'Question {{current}} of {{total}}',
        timeRemaining: 'Time Remaining: {{time}}',
        thinkingTime: 'Thinking Time: {{time}}',
        recordingTime: 'Recording Time: {{time}}',
        textAnswer: 'Your Answer',
        voiceAnswer: 'Voice Answer',
        startRecording: 'Start Recording',
        stopRecording: 'Stop Recording',
        recording: 'Recording...',
        processing: 'Processing...',
        transcript: 'Transcript',
        nextQuestion: 'Next Question',
        previousQuestion: 'Previous Question',
        skipQuestion: 'Skip Question',
        rephraseQuestion: 'Rephrase Question',
        submitAnswer: 'Submit Answer',
        completedInterview: 'Interview Completed'
      },
      
      types: {
        technical: 'Technical Question',
        behavioral: 'Behavioral Question',
        situational: 'Situational Question',
        coding: 'Coding Challenge',
        resume: 'Resume-based Question'
      },
      
      feedback: {
        title: 'Interview Feedback',
        score: 'Overall Score: {{score}}%',
        strengths: 'Strengths',
        improvements: 'Areas for Improvement',
        recommendations: 'Recommendations',
        technicalScore: 'Technical Score: {{score}}%',
        behavioralScore: 'Behavioral Score: {{score}}%',
        communicationScore: 'Communication Score: {{score}}%'
      }
    },
    
    admin: {
      dashboard: {
        title: 'Elite Interview Dashboard',
        logout: 'Logout',
        tabs: {
          createInterview: 'Create Interview',
          candidatePipeline: 'Candidate Pipeline',
          assessmentReports: 'Assessment Reports',
          comparison: 'Comparison'
        }
      },
      
      createInterview: {
        title: 'Create Enhanced Interview Token',
        jobTitle: 'Job Title',
        jobTitlePlaceholder: 'e.g., Senior Frontend Developer',
        roleArchetype: 'Role Archetype',
        interviewFocus: 'Interview Focus',
        codingChallenge: 'Include Coding Challenge',
        jobDescription: 'Job Description',
        jobDescriptionPlaceholder: 'Detailed job description...',
        jobRequirements: 'Job Requirements',
        jobRequirementsPlaceholder: 'Technical skills, experience requirements...',
        resumeFile: 'Resume File',
        
        questionConfig: {
          title: 'Interview Questions Configuration',
          subtitle: 'Set the range of questions to be asked during the interview. The system will dynamically adjust based on candidate responses.',
          minQuestions: 'Minimum Questions',
          maxQuestions: 'Maximum Questions',
          estimatedDuration: 'Estimated Interview Duration: {{min}} - {{max}} minutes',
          distribution: 'Expected Question Distribution',
          technical: 'Technical Questions: {{min}} - {{max}}',
          behavioral: 'Behavioral Questions: {{min}} - {{max}}'
        },
        
        customQuestions: {
          title: 'Question Selection Controls',
          subtitle: 'Customize your interview questions by specifying counts and choosing between AI-generated or manually entered questions.',
          totalQuestions: 'Total Questions: {{total}} / {{min}}-{{max}}',
          warningOutOfRange: 'Total questions must be between {{min}} and {{max}}',
          
          resumeBased: 'Resume-Based Questions',
          technical: 'Technical Questions',
          behavioral: 'Behavioral Questions',
          
          numberOfQuestions: 'Number of Questions',
          questionType: 'Question Type',
          autoGenerate: 'Auto-generate via AI',
          manualEntry: 'Manually enter questions',
          
          manualQuestions: 'Manual {{type}} Questions',
          questionPlaceholder: 'Enter your {{type}} question...',
          expectedAnswer: 'Expected Answer (Optional)',
          expectedAnswerPlaceholder: 'Enter expected answer (optional)...'
        },
        
        createButton: 'Create Interview Token',
        creating: 'Creating...',
        
        success: {
          title: 'Interview Token Created Successfully',
          token: 'Interview Token: {{token}}',
          copyToken: 'Copy Token',
          tokenCopied: 'Token copied to clipboard!',
          candidateInstructions: 'Share this token with the candidate',
          features: 'Interview Features',
          createAnother: 'Create Another Interview'
        },
        
        errors: {
          invalidQuestionCount: 'Total questions must be between {{min}} and {{max}}. Current total: {{current}}',
          uploadFailed: 'Upload failed: {{error}}',
          generalError: 'Upload failed. Please try again.'
        }
      },
      
      candidatePipeline: {
        title: 'Candidate Pipeline',
        total: 'Total Candidates: {{count}}',
        search: 'Search candidates...',
        filters: {
          all: 'All',
          invited: 'Invited',
          inProgress: 'In Progress',
          completed: 'Completed',
          reportReady: 'Report Ready'
        },
        
        table: {
          name: 'Name',
          position: 'Position',
          status: 'Status',
          score: 'Score',
          date: 'Date',
          actions: 'Actions'
        },
        
        actions: {
          viewReport: 'View Report',
          compare: 'Compare',
          resendInvite: 'Resend Invite',
          archive: 'Archive'
        },
        
        comparison: {
          title: 'Candidate Comparison',
          selectCandidates: 'Select candidates to compare',
          compareButton: 'Compare Selected',
          minCandidates: 'Please select at least 2 candidates to compare'
        }
      },
      
      reports: {
        title: 'Assessment Reports',
        downloadReport: 'Download Report',
        viewDetails: 'View Details',
        
        summary: {
          overallScore: 'Overall Score',
          technicalScore: 'Technical Score',
          behavioralScore: 'Behavioral Score',
          communicationScore: 'Communication Score',
          recommendationScore: 'Recommendation Score'
        },
        
        details: {
          candidateInfo: 'Candidate Information',
          interviewMetrics: 'Interview Metrics',
          questionAnalysis: 'Question Analysis',
          recommendations: 'Recommendations',
          biasAnalysis: 'Bias Analysis'
        }
      }
    },
    
    accessibility: {
      title: 'Accessibility Settings',
      subtitle: 'Customize your viewing experience',
      
      settings: {
        highContrast: 'High Contrast Mode',
        highContrastDescription: 'Increases contrast for better visibility',
        
        fontSize: 'Font Size',
        fontSizeOptions: {
          small: 'Small',
          medium: 'Medium',
          large: 'Large',
          xlarge: 'Extra Large'
        },
        
        reduceMotion: 'Reduce Motion',
        reduceMotionDescription: 'Minimizes animations and transitions',
        
        screenReader: 'Screen Reader Mode',
        screenReaderDescription: 'Optimizes interface for screen readers',
        
        keyboardNavigation: 'Keyboard Navigation',
        keyboardNavigationDescription: 'Enhanced keyboard shortcuts and navigation',
        
        announcements: 'Screen Reader Announcements',
        announcementsDescription: 'Announces changes and updates'
      },
      
      shortcuts: {
        title: 'Keyboard Shortcuts',
        highContrast: 'Alt + H: Toggle high contrast',
        fontSize: 'Alt + +/-: Adjust font size',
        reduceMotion: 'Alt + M: Toggle reduced motion',
        reset: 'Alt + R: Reset settings'
      },
      
      reset: 'Reset to Default',
      
      announcements: {
        highContrastEnabled: 'High contrast mode enabled',
        highContrastDisabled: 'High contrast mode disabled',
        fontSizeChanged: 'Font size changed to {{size}}',
        reduceMotionEnabled: 'Reduce motion enabled',
        reduceMotionDisabled: 'Reduce motion disabled',
        screenReaderEnabled: 'Screen reader optimizations enabled',
        screenReaderDisabled: 'Screen reader optimizations disabled',
        keyboardNavigationEnabled: 'Keyboard navigation enabled',
        keyboardNavigationDisabled: 'Keyboard navigation disabled',
        settingsReset: 'Accessibility settings reset to default',
        panelOpened: 'Accessibility panel opened',
        panelClosed: 'Accessibility panel closed',
        panelExpanded: 'Accessibility panel expanded',
        panelCollapsed: 'Accessibility panel collapsed'
      },
      
      languageChanged: 'Language changed to {{language}}'
    },
    
    pwa: {
      install: {
        title: 'Install App',
        message: 'Install this app on your device for a better experience',
        button: 'Install',
        cancel: 'Maybe Later',
        success: 'App installed successfully',
        error: 'Failed to install app'
      },
      
      offline: {
        title: 'You are offline',
        message: 'Some features may be limited while offline',
        retry: 'Retry Connection'
      },
      
      update: {
        title: 'Update Available',
        message: 'A new version is available. Would you like to update?',
        update: 'Update Now',
        later: 'Later'
      }
    },
    
    time: {
      justNow: 'Just now',
      minutesAgo: '{{minutes}} minutes ago',
      hoursAgo: '{{hours}} hours ago',
      daysAgo: '{{days}} days ago'
    },
    
    errors: {
      generic: 'An error occurred. Please try again.',
      network: 'Network error. Please check your connection.',
      timeout: 'Request timed out. Please try again.',
      unauthorized: 'Unauthorized access.',
      forbidden: 'Access forbidden.',
      notFound: 'Resource not found.',
      serverError: 'Server error. Please try again later.',
      validationError: 'Validation error. Please check your input.',
      
      interview: {
        failedToStart: 'Failed to start interview',
        failedToSubmit: 'Failed to submit answer',
        failedToLoad: 'Failed to load interview',
        cameraAccess: 'Camera access denied. Please allow camera access.',
        microphoneAccess: 'Microphone access denied. Please allow microphone access.',
        voiceRecognition: 'Voice recognition error. Please try again.',
        uploadFailed: 'File upload failed. Please try again.'
      }
    }
  },
  
  es: {
    common: {
      loading: 'Cargando...',
      error: 'Error',
      success: 'Éxito',
      cancel: 'Cancelar',
      confirm: 'Confirmar',
      close: 'Cerrar',
      save: 'Guardar',
      edit: 'Editar',
      delete: 'Eliminar',
      back: 'Atrás',
      next: 'Siguiente',
      previous: 'Anterior',
      submit: 'Enviar',
      reset: 'Reiniciar',
      search: 'Buscar',
      filter: 'Filtrar',
      sort: 'Ordenar',
      refresh: 'Actualizar',
      download: 'Descargar',
      upload: 'Subir',
      print: 'Imprimir',
      share: 'Compartir',
      copy: 'Copiar',
      paste: 'Pegar',
      cut: 'Cortar',
      select: 'Seleccionar',
      selectAll: 'Seleccionar Todo',
      clear: 'Limpiar',
      apply: 'Aplicar',
      ok: 'OK',
      yes: 'Sí',
      no: 'No'
    },
    
    navigation: {
      home: 'Inicio',
      about: 'Acerca de',
      contact: 'Contacto',
      help: 'Ayuda',
      settings: 'Configuración',
      profile: 'Perfil',
      logout: 'Cerrar Sesión',
      login: 'Iniciar Sesión',
      register: 'Registrarse',
      dashboard: 'Panel de Control',
      reports: 'Reportes',
      admin: 'Administrador',
      candidate: 'Candidato'
    },
    
    landing: {
      title: 'Plataforma de Entrevistas AI Elite',
      subtitle: 'Experimenta el futuro de la contratación con nuestro sistema avanzado de entrevistas con IA. Incluye desafíos de codificación interactivos, flujo de trabajo empático para candidatos, evaluaciones multi-vectoriales y controles integrales de mitigación de sesgos.',
      features: {
        codingChallenges: 'Desafíos de Codificación Interactivos',
        voiceInterview: 'Entrevista de Voz con IA',
        multiVectorAssessment: 'Evaluaciones Multi-Vectoriales',
        biasMitigation: 'Controles de Mitigación de Sesgos'
      },
      adminPortal: {
        title: 'Panel de Administración',
        description: 'Gestión integral de contratación con pipeline de candidatos, personalización de entrevistas, desafíos de codificación y reportes avanzados multi-vectoriales con controles de sesgo.',
        features: {
          candidatePipeline: 'Pipeline y Herramientas de Comparación de Candidatos',
          roleArchetypes: 'Arquetipos de Roles y Enfoque de Entrevista',
          codingChallenges: 'Desafíos de Codificación Interactivos'
        },
        button: 'Acceder al Portal de Administración'
      },
      candidatePortal: {
        title: 'Experiencia del Candidato',
        description: 'Experiencia de entrevista interactiva y empática con configuración guiada, rondas de práctica, controles de preguntas y cuestionamiento adaptativo de IA para una evaluación justa.',
        features: {
          setupCheck: 'Verificación de Cámara/Micrófono y Ronda de Práctica',
          questionCards: 'Tarjetas de Preguntas con Tiempo de Reflexión',
          interactiveModules: 'Módulos Interactivos y Tareas de Codificación'
        },
        button: 'Iniciar Experiencia de Entrevista'
      },
      placementPreparation: {
        title: 'Preparación para Colocación',
        description: 'Herramientas integrales de preparación para colocación con creación de entrevistas, sesiones de práctica y evaluación de habilidades para ayudarte a prepararte para el trabajo de tus sueños.',
        features: {
          createInterview: 'Crear Entrevistas Personalizadas',
          practiceRounds: 'Práctica y Sesiones Simuladas',
          skillAssessment: 'Herramientas de Evaluación de Habilidades'
        },
        button: 'Comenzar Preparación'
      }
    },
    
    auth: {
      adminLogin: {
        title: 'Inicio de Sesión de Administrador',
        subtitle: 'Ingresa tus credenciales de administrador para continuar',
        passwordLabel: 'Contraseña de Administrador',
        passwordPlaceholder: 'Ingresa la contraseña de administrador',
        loginButton: 'Iniciar Sesión',
        loggingIn: 'Iniciando sesión...',
        backToHome: 'Volver al Inicio',
        errors: {
          invalidPassword: 'Contraseña inválida',
          connectionError: 'Error de conexión'
        }
      },
      candidateLogin: {
        title: 'Portal del Candidato',
        subtitle: 'Ingresa tu token de entrevista para comenzar',
        tokenLabel: 'Token de Entrevista',
        tokenPlaceholder: 'Ingresa tu token de entrevista',
        startButton: 'Iniciar Entrevista',
        starting: 'Iniciando...',
        backToHome: 'Volver al Inicio',
        errors: {
          invalidToken: 'Token inválido',
          connectionError: 'Error de conexión'
        }
      }
    },
    
    accessibility: {
      title: 'Configuración de Accesibilidad',
      subtitle: 'Personaliza tu experiencia de visualización',
      
      settings: {
        highContrast: 'Modo de Alto Contraste',
        highContrastDescription: 'Aumenta el contraste para mejor visibilidad',
        
        fontSize: 'Tamaño de Fuente',
        fontSizeOptions: {
          small: 'Pequeño',
          medium: 'Mediano',
          large: 'Grande',
          xlarge: 'Extra Grande'
        },
        
        reduceMotion: 'Reducir Movimiento',
        reduceMotionDescription: 'Minimiza animaciones y transiciones',
        
        screenReader: 'Modo de Lector de Pantalla',
        screenReaderDescription: 'Optimiza la interfaz para lectores de pantalla',
        
        keyboardNavigation: 'Navegación por Teclado',
        keyboardNavigationDescription: 'Atajos de teclado y navegación mejorados',
        
        announcements: 'Anuncios del Lector de Pantalla',
        announcementsDescription: 'Anuncia cambios y actualizaciones'
      },
      
      shortcuts: {
        title: 'Atajos de Teclado',
        highContrast: 'Alt + H: Alternar alto contraste',
        fontSize: 'Alt + +/-: Ajustar tamaño de fuente',
        reduceMotion: 'Alt + M: Alternar reducción de movimiento',
        reset: 'Alt + R: Restablecer configuración'
      },
      
      reset: 'Restablecer a Predeterminado',
      
      announcements: {
        highContrastEnabled: 'Modo de alto contraste activado',
        highContrastDisabled: 'Modo de alto contraste desactivado',
        fontSizeChanged: 'Tamaño de fuente cambiado a {{size}}',
        reduceMotionEnabled: 'Reducción de movimiento activada',
        reduceMotionDisabled: 'Reducción de movimiento desactivada',
        screenReaderEnabled: 'Optimizaciones de lector de pantalla activadas',
        screenReaderDisabled: 'Optimizaciones de lector de pantalla desactivadas',
        keyboardNavigationEnabled: 'Navegación por teclado activada',
        keyboardNavigationDisabled: 'Navegación por teclado desactivada',
        settingsReset: 'Configuración de accesibilidad restablecida a predeterminado',
        panelOpened: 'Panel de accesibilidad abierto',
        panelClosed: 'Panel de accesibilidad cerrado',
        panelExpanded: 'Panel de accesibilidad expandido',
        panelCollapsed: 'Panel de accesibilidad contraído'
      },
      
      languageChanged: 'Idioma cambiado a {{language}}'
    },
    
    pwa: {
      install: {
        title: 'Instalar Aplicación',
        message: 'Instala esta aplicación en tu dispositivo para una mejor experiencia',
        button: 'Instalar',
        cancel: 'Quizás Más Tarde',
        success: 'Aplicación instalada exitosamente',
        error: 'Error al instalar la aplicación'
      },
      
      offline: {
        title: 'Estás desconectado',
        message: 'Algunas funciones pueden estar limitadas sin conexión',
        retry: 'Reintentar Conexión'
      },
      
      update: {
        title: 'Actualización Disponible',
        message: 'Una nueva versión está disponible. ¿Te gustaría actualizar?',
        update: 'Actualizar Ahora',
        later: 'Más Tarde'
      }
    },
    
    time: {
      justNow: 'Justo ahora',
      minutesAgo: 'hace {{minutes}} minutos',
      hoursAgo: 'hace {{hours}} horas',
      daysAgo: 'hace {{days}} días'
    },
    
    errors: {
      generic: 'Ocurrió un error. Por favor intenta de nuevo.',
      network: 'Error de red. Por favor verifica tu conexión.',
      timeout: 'Tiempo de espera agotado. Por favor intenta de nuevo.',
      unauthorized: 'Acceso no autorizado.',
      forbidden: 'Acceso prohibido.',
      notFound: 'Recurso no encontrado.',
      serverError: 'Error del servidor. Por favor intenta más tarde.',
      validationError: 'Error de validación. Por favor verifica tu entrada.',
      
      interview: {
        failedToStart: 'Error al iniciar la entrevista',
        failedToSubmit: 'Error al enviar la respuesta',
        failedToLoad: 'Error al cargar la entrevista',
        cameraAccess: 'Acceso a cámara denegado. Por favor permite el acceso a la cámara.',
        microphoneAccess: 'Acceso a micrófono denegado. Por favor permite el acceso al micrófono.',
        voiceRecognition: 'Error de reconocimiento de voz. Por favor intenta de nuevo.',
        uploadFailed: 'Error al subir archivo. Por favor intenta de nuevo.'
      }
    }
  },
  
  fr: {
    common: {
      loading: 'Chargement...',
      error: 'Erreur',
      success: 'Succès',
      cancel: 'Annuler',
      confirm: 'Confirmer',
      close: 'Fermer',
      save: 'Sauvegarder',
      edit: 'Modifier',
      delete: 'Supprimer',
      back: 'Retour',
      next: 'Suivant',
      previous: 'Précédent',
      submit: 'Soumettre',
      reset: 'Réinitialiser',
      search: 'Rechercher',
      filter: 'Filtrer',
      sort: 'Trier',
      refresh: 'Actualiser',
      download: 'Télécharger',
      upload: 'Uploader',
      print: 'Imprimer',
      share: 'Partager',
      copy: 'Copier',
      paste: 'Coller',
      cut: 'Couper',
      select: 'Sélectionner',
      selectAll: 'Tout Sélectionner',
      clear: 'Effacer',
      apply: 'Appliquer',
      ok: 'OK',
      yes: 'Oui',
      no: 'Non'
    },
    
    navigation: {
      home: 'Accueil',
      about: 'À propos',
      contact: 'Contact',
      help: 'Aide',
      settings: 'Paramètres',
      profile: 'Profil',
      logout: 'Déconnexion',
      login: 'Connexion',
      register: "S'inscrire",
      dashboard: 'Tableau de Bord',
      reports: 'Rapports',
      admin: 'Administrateur',
      candidate: 'Candidat'
    },
    
    landing: {
      title: "Plateforme d'Entretien IA Elite",
      subtitle: "Découvrez l'avenir du recrutement avec notre système d'entretien avancé alimenté par l'IA. Comprend des défis de codage interactifs, un flux de travail empathique pour les candidats, des évaluations multi-vectorielles et des contrôles complets d'atténuation des biais.",
      features: {
        codingChallenges: 'Défis de Codage Interactifs',
        voiceInterview: 'Entretien Vocal avec IA',
        multiVectorAssessment: 'Évaluations Multi-Vectorielles',
        biasMitigation: "Contrôles d'Atténuation des Biais"
      },
      adminPortal: {
        title: "Tableau de Bord d'Administration",
        description: 'Gestion complète du recrutement avec pipeline de candidats, personnalisation des entretiens, défis de codage et rapports avancés multi-vectoriels avec contrôles de biais.',
        features: {
          candidatePipeline: 'Pipeline et Outils de Comparaison de Candidats',
          roleArchetypes: "Archétypes de Rôles et Focus d'Entretien",
          codingChallenges: 'Défis de Codage Interactifs'
        },
        button: "Accéder au Portail d'Administration"
      },
      candidatePortal: {
        title: 'Expérience du Candidat',
        description: "Expérience d'entretien interactive et empathique avec configuration guidée, tours de pratique, contrôles de questions et questionnement adaptatif de l'IA pour une évaluation équitable.",
        features: {
          setupCheck: 'Vérification Caméra/Micro et Tour de Pratique',
          questionCards: 'Cartes de Questions avec Temps de Réflexion',
          interactiveModules: 'Modules Interactifs et Tâches de Codage'
        },
        button: "Commencer l'Expérience d'Entretien"
      }
    },
    
    auth: {
      adminLogin: {
        title: "Connexion d'Administrateur",
        subtitle: "Entrez vos identifiants d'administrateur pour continuer",
        passwordLabel: "Mot de Passe d'Administrateur",
        passwordPlaceholder: "Entrez le mot de passe d'administrateur",
        loginButton: 'Se Connecter',
        loggingIn: 'Connexion en cours...',
        backToHome: "Retour à l'Accueil",
        errors: {
          invalidPassword: 'Mot de passe invalide',
          connectionError: 'Erreur de connexion'
        }
      },
      candidateLogin: {
        title: 'Portail du Candidat',
        subtitle: "Entrez votre jeton d'entretien pour commencer",
        tokenLabel: "Jeton d'Entretien",
        tokenPlaceholder: "Entrez votre jeton d'entretien",
        startButton: 'Commencer l\'Entretien',
        starting: 'Démarrage...',
        backToHome: "Retour à l'Accueil",
        errors: {
          invalidToken: 'Jeton invalide',
          connectionError: 'Erreur de connexion'
        }
      }
    },
    
    accessibility: {
      title: "Paramètres d'Accessibilité",
      subtitle: 'Personnalisez votre expérience de visualisation',
      
      settings: {
        highContrast: 'Mode Haut Contraste',
        highContrastDescription: 'Augmente le contraste pour une meilleure visibilité',
        
        fontSize: 'Taille de Police',
        fontSizeOptions: {
          small: 'Petit',
          medium: 'Moyen',
          large: 'Grand',
          xlarge: 'Très Grand'
        },
        
        reduceMotion: 'Réduire le Mouvement',
        reduceMotionDescription: 'Minimise les animations et transitions',
        
        screenReader: "Mode Lecteur d'Écran",
        screenReaderDescription: "Optimise l'interface pour les lecteurs d'écran",
        
        keyboardNavigation: 'Navigation au Clavier',
        keyboardNavigationDescription: 'Raccourcis clavier et navigation améliorés',
        
        announcements: "Annonces du Lecteur d'Écran",
        announcementsDescription: 'Annonce les changements et mises à jour'
      },
      
      shortcuts: {
        title: 'Raccourcis Clavier',
        highContrast: 'Alt + H: Basculer le haut contraste',
        fontSize: 'Alt + +/-: Ajuster la taille de police',
        reduceMotion: 'Alt + M: Basculer la réduction de mouvement',
        reset: 'Alt + R: Réinitialiser les paramètres'
      },
      
      reset: 'Réinitialiser par Défaut',
      
      announcements: {
        highContrastEnabled: 'Mode haut contraste activé',
        highContrastDisabled: 'Mode haut contraste désactivé',
        fontSizeChanged: 'Taille de police changée à {{size}}',
        reduceMotionEnabled: 'Réduction de mouvement activée',
        reduceMotionDisabled: 'Réduction de mouvement désactivée',
        screenReaderEnabled: "Optimisations du lecteur d'écran activées",
        screenReaderDisabled: "Optimisations du lecteur d'écran désactivées",
        keyboardNavigationEnabled: 'Navigation au clavier activée',
        keyboardNavigationDisabled: 'Navigation au clavier désactivée',
        settingsReset: "Paramètres d'accessibilité réinitialisés par défaut",
        panelOpened: "Panneau d'accessibilité ouvert",
        panelClosed: "Panneau d'accessibilité fermé",
        panelExpanded: "Panneau d'accessibilité étendu",
        panelCollapsed: "Panneau d'accessibilité réduit"
      },
      
      languageChanged: 'Langue changée à {{language}}'
    },
    
    pwa: {
      install: {
        title: 'Installer l\'Application',
        message: 'Installez cette application sur votre appareil pour une meilleure expérience',
        button: 'Installer',
        cancel: 'Peut-être Plus Tard',
        success: 'Application installée avec succès',
        error: "Échec de l'installation de l'application"
      },
      
      offline: {
        title: 'Vous êtes hors ligne',
        message: 'Certaines fonctionnalités peuvent être limitées hors ligne',
        retry: 'Réessayer la Connexion'
      },
      
      update: {
        title: 'Mise à Jour Disponible',
        message: 'Une nouvelle version est disponible. Souhaitez-vous mettre à jour?',
        update: 'Mettre à Jour Maintenant',
        later: 'Plus Tard'
      }
    },
    
    time: {
      justNow: 'À l\'instant',
      minutesAgo: 'il y a {{minutes}} minutes',
      hoursAgo: 'il y a {{hours}} heures',
      daysAgo: 'il y a {{days}} jours'
    },
    
    errors: {
      generic: 'Une erreur s\'est produite. Veuillez réessayer.',
      network: 'Erreur réseau. Veuillez vérifier votre connexion.',
      timeout: 'Délai d\'attente dépassé. Veuillez réessayer.',
      unauthorized: 'Accès non autorisé.',
      forbidden: 'Accès interdit.',
      notFound: 'Ressource non trouvée.',
      serverError: 'Erreur serveur. Veuillez réessayer plus tard.',
      validationError: 'Erreur de validation. Veuillez vérifier votre saisie.',
      
      interview: {
        failedToStart: 'Échec du démarrage de l\'entretien',
        failedToSubmit: 'Échec de l\'envoi de la réponse',
        failedToLoad: 'Échec du chargement de l\'entretien',
        cameraAccess: 'Accès à la caméra refusé. Veuillez autoriser l\'accès à la caméra.',
        microphoneAccess: 'Accès au microphone refusé. Veuillez autoriser l\'accès au microphone.',
        voiceRecognition: 'Erreur de reconnaissance vocale. Veuillez réessayer.',
        uploadFailed: 'Échec du téléchargement du fichier. Veuillez réessayer.'
      }
    }
  },
  
  // Adding placeholder structures for other languages
  de: {
    common: {
      loading: 'Lädt...',
      error: 'Fehler',
      success: 'Erfolgreich',
      cancel: 'Abbrechen',
      confirm: 'Bestätigen',
      close: 'Schließen',
      save: 'Speichern',
      edit: 'Bearbeiten',
      delete: 'Löschen',
      back: 'Zurück',
      next: 'Weiter',
      previous: 'Zurück',
      submit: 'Einreichen',
      reset: 'Zurücksetzen',
      search: 'Suchen',
      filter: 'Filter',
      sort: 'Sortieren',
      refresh: 'Aktualisieren',
      download: 'Herunterladen',
      upload: 'Hochladen',
      print: 'Drucken',
      share: 'Teilen',
      copy: 'Kopieren',
      paste: 'Einfügen',
      cut: 'Ausschneiden',
      select: 'Auswählen',
      selectAll: 'Alle auswählen',
      clear: 'Löschen',
      apply: 'Anwenden',
      ok: 'OK',
      yes: 'Ja',
      no: 'Nein'
    },
    
    navigation: {
      home: 'Startseite',
      about: 'Über uns',
      contact: 'Kontakt',
      help: 'Hilfe',
      settings: 'Einstellungen',
      profile: 'Profil',
      logout: 'Abmelden',
      login: 'Anmelden',
      register: 'Registrieren',
      dashboard: 'Dashboard',
      reports: 'Berichte',
      admin: 'Administrator',
      candidate: 'Kandidat'
    },
    
    landing: {
      title: 'Elite KI-Interview-Plattform',
      subtitle: 'Erleben Sie die Zukunft der Personalbeschaffung mit unserem fortschrittlichen KI-gestützten Interview-System. Bietet interaktive Coding-Herausforderungen, empathischen Kandidaten-Workflow, Multi-Vektor-Bewertungen und umfassende Bias-Mitigations-Kontrollen.',
      features: {
        codingChallenges: 'Interaktive Coding-Herausforderungen',
        voiceInterview: 'Sprach-Interview mit KI',
        multiVectorAssessment: 'Multi-Vektor-Bewertungen',
        biasMitigation: 'Bias-Mitigations-Kontrollen'
      },
      adminPortal: {
        title: 'Admin-Dashboard',
        description: 'Umfassendes Personalmanagement mit Kandidaten-Pipeline, Interview-Anpassung, Coding-Herausforderungen und erweiterten Multi-Vektor-Berichten mit Bias-Kontrollen.',
        features: {
          candidatePipeline: 'Kandidaten-Pipeline & Vergleichstools',
          roleArchetypes: 'Rollen-Archetypen & Interview-Fokus',
          codingChallenges: 'Interaktive Coding-Herausforderungen'
        },
        button: 'Admin-Portal aufrufen'
      },
      candidatePortal: {
        title: 'Kandidaten-Erfahrung',
        description: 'Interaktive und empathische Interview-Erfahrung mit geführter Einrichtung, Übungsrunden, Fragen-Kontrollen und adaptivem KI-Befragung für eine faire Bewertung.',
        features: {
          setupCheck: 'Kamera-/Mikrofon-Check & Übungsrunde',
          questionCards: 'Fragenkarten mit Denkzeit',
          interactiveModules: 'Interaktive Module & Coding-Aufgaben'
        },
        button: 'Interview-Erfahrung starten'
      }
    },
    
    accessibility: {
      title: 'Barrierefreiheit-Einstellungen',
      subtitle: 'Passen Sie Ihr Seherlebnis an',
      
      settings: {
        highContrast: 'Hoher Kontrast Modus',
        highContrastDescription: 'Erhöht den Kontrast für bessere Sichtbarkeit',
        
        fontSize: 'Schriftgröße',
        fontSizeOptions: {
          small: 'Klein',
          medium: 'Mittel',
          large: 'Groß',
          xlarge: 'Extra Groß'
        },
        
        reduceMotion: 'Bewegung reduzieren',
        reduceMotionDescription: 'Minimiert Animationen und Übergänge',
        
        screenReader: 'Bildschirmleser-Modus',
        screenReaderDescription: 'Optimiert die Oberfläche für Bildschirmleser',
        
        keyboardNavigation: 'Tastaturnavigation',
        keyboardNavigationDescription: 'Erweiterte Tastaturkürzel und Navigation',
        
        announcements: 'Bildschirmleser-Ansagen',
        announcementsDescription: 'Kündigt Änderungen und Updates an'
      },
      
      shortcuts: {
        title: 'Tastaturkürzel',
        highContrast: 'Alt + H: Hohen Kontrast umschalten',
        fontSize: 'Alt + +/-: Schriftgröße anpassen',
        reduceMotion: 'Alt + M: Bewegungsreduzierung umschalten',
        reset: 'Alt + R: Einstellungen zurücksetzen'
      },
      
      reset: 'Auf Standard zurücksetzen',
      
      announcements: {
        highContrastEnabled: 'Hoher Kontrast Modus aktiviert',
        highContrastDisabled: 'Hoher Kontrast Modus deaktiviert',
        fontSizeChanged: 'Schriftgröße geändert auf {{size}}',
        reduceMotionEnabled: 'Bewegungsreduzierung aktiviert',
        reduceMotionDisabled: 'Bewegungsreduzierung deaktiviert',
        screenReaderEnabled: 'Bildschirmleser-Optimierungen aktiviert',
        screenReaderDisabled: 'Bildschirmleser-Optimierungen deaktiviert',
        keyboardNavigationEnabled: 'Tastaturnavigation aktiviert',
        keyboardNavigationDisabled: 'Tastaturnavigation deaktiviert',
        settingsReset: 'Barrierefreiheit-Einstellungen auf Standard zurückgesetzt',
        panelOpened: 'Barrierefreiheit-Panel geöffnet',
        panelClosed: 'Barrierefreiheit-Panel geschlossen',
        panelExpanded: 'Barrierefreiheit-Panel erweitert',
        panelCollapsed: 'Barrierefreiheit-Panel eingeklappt'
      },
      
      languageChanged: 'Sprache geändert zu {{language}}'
    },
    
    pwa: {
      install: {
        title: 'App installieren',
        message: 'Installieren Sie diese App auf Ihrem Gerät für eine bessere Erfahrung',
        button: 'Installieren',
        cancel: 'Vielleicht später',
        success: 'App erfolgreich installiert',
        error: 'Fehler beim Installieren der App'
      },
      
      offline: {
        title: 'Sie sind offline',
        message: 'Einige Funktionen können offline eingeschränkt sein',
        retry: 'Verbindung erneut versuchen'
      },
      
      update: {
        title: 'Update verfügbar',
        message: 'Eine neue Version ist verfügbar. Möchten Sie aktualisieren?',
        update: 'Jetzt aktualisieren',
        later: 'Später'
      }
    },
    
    time: {
      justNow: 'Gerade eben',
      minutesAgo: 'vor {{minutes}} Minuten',
      hoursAgo: 'vor {{hours}} Stunden',
      daysAgo: 'vor {{days}} Tagen'
    },
    
    errors: {
      generic: 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.',
      network: 'Netzwerkfehler. Bitte überprüfen Sie Ihre Verbindung.',
      timeout: 'Zeitüberschreitung. Bitte versuchen Sie es erneut.',
      unauthorized: 'Unbefugter Zugriff.',
      forbidden: 'Zugriff verweigert.',
      notFound: 'Ressource nicht gefunden.',
      serverError: 'Serverfehler. Bitte versuchen Sie es später erneut.',
      validationError: 'Validierungsfehler. Bitte überprüfen Sie Ihre Eingabe.',
      
      interview: {
        failedToStart: 'Interview konnte nicht gestartet werden',
        failedToSubmit: 'Antwort konnte nicht übermittelt werden',
        failedToLoad: 'Interview konnte nicht geladen werden',
        cameraAccess: 'Kamera-Zugriff verweigert. Bitte erlauben Sie Kamera-Zugriff.',
        microphoneAccess: 'Mikrofon-Zugriff verweigert. Bitte erlauben Sie Mikrofon-Zugriff.',
        voiceRecognition: 'Spracherkennung-Fehler. Bitte versuchen Sie es erneut.',
        uploadFailed: 'Datei-Upload fehlgeschlagen. Bitte versuchen Sie es erneut.'
      }
    }
  },
  
  // Placeholder structures for remaining languages
  it: {
    common: { loading: 'Caricamento...' },
    navigation: { home: 'Home' },
    landing: { title: 'Piattaforma Elite AI Interview' },
    accessibility: { title: 'Impostazioni di Accessibilità' },
    pwa: { install: { title: 'Installa App' } },
    time: { justNow: 'Proprio ora' },
    errors: { generic: 'Si è verificato un errore. Riprova.' }
  },
  
  pt: {
    common: { loading: 'Carregando...' },
    navigation: { home: 'Início' },
    landing: { title: 'Plataforma Elite de Entrevista com IA' },
    accessibility: { title: 'Configurações de Acessibilidade' },
    pwa: { install: { title: 'Instalar App' } },
    time: { justNow: 'Agora mesmo' },
    errors: { generic: 'Ocorreu um erro. Tente novamente.' }
  },
  
  ja: {
    common: { loading: '読み込み中...' },
    navigation: { home: 'ホーム' },
    landing: { title: 'エリートAI面接プラットフォーム' },
    accessibility: { title: 'アクセシビリティ設定' },
    pwa: { install: { title: 'アプリをインストール' } },
    time: { justNow: 'たった今' },
    errors: { generic: 'エラーが発生しました。もう一度お試しください。' }
  },
  
  zh: {
    common: { loading: '加载中...' },
    navigation: { home: '首页' },
    landing: { title: '精英AI面试平台' },
    accessibility: { title: '辅助功能设置' },
    pwa: { install: { title: '安装应用' } },
    time: { justNow: '刚刚' },
    errors: { generic: '发生错误。请重试。' }
  }
};